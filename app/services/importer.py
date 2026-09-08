import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import bindparam, func, select, update
from sqlalchemy.dialects.postgresql import insert

from app.database.database import SessionLocal
from app.database.models import Message, User

BATCH_SIZE = 500
SUPERGROUP_ID_OFFSET = 1_000_000_000_000


@dataclass
class MembershipAnalysis:
    joined_at_by_user: dict[int, datetime] = field(default_factory=dict)
    link_events: int = 0
    invite_references: int = 0
    resolved_invites: int = 0
    ambiguous_invites: int = 0
    unmatched_invites: int = 0


def parse_text(text) -> str:
    if isinstance(text, str):
        return text

    if isinstance(text, list):
        return "".join(
            part if isinstance(part, str) else part.get("text", "")
            for part in text
            if isinstance(part, (str, dict))
        )

    return ""


def parse_user_id(from_id: object) -> int | None:
    if not isinstance(from_id, str) or not from_id.startswith("user"):
        return None

    value = from_id.removeprefix("user")
    return int(value) if value.isdigit() else None


def parse_export_datetime(item: dict) -> datetime:
    timestamp = item.get("date_unixtime")
    if timestamp is not None:
        try:
            return datetime.fromtimestamp(int(timestamp), UTC)
        except (TypeError, ValueError, OSError):
            pass

    value = datetime.fromisoformat(item["date"])
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)


def normalize_export_chat_id(chat_id: int, chat_type: str | None) -> int:
    if chat_id > 0 and chat_type in {
        "channel",
        "private_channel",
        "private_supergroup",
        "supergroup",
    }:
        return -(SUPERGROUP_ID_OFFSET + chat_id)
    return chat_id


def _add_alias(
    aliases: dict[str, set[int]],
    name: object,
    telegram_reference: object,
) -> None:
    telegram_id = parse_user_id(telegram_reference)
    if telegram_id is None or not isinstance(name, str) or not name:
        return
    aliases.setdefault(name, set()).add(telegram_id)


def analyze_membership_events(
    messages: list[dict],
    known_aliases: dict[str, set[int]] | None = None,
) -> MembershipAnalysis:
    aliases = {
        name: set(telegram_ids)
        for name, telegram_ids in (known_aliases or {}).items()
    }
    for item in messages:
        if item.get("type") == "message":
            _add_alias(aliases, item.get("from"), item.get("from_id"))
        elif item.get("type") == "service":
            _add_alias(aliases, item.get("actor"), item.get("actor_id"))

    analysis = MembershipAnalysis()

    def record(telegram_id: int, joined_at: datetime) -> None:
        previous = analysis.joined_at_by_user.get(telegram_id)
        if previous is None or joined_at < previous:
            analysis.joined_at_by_user[telegram_id] = joined_at

    for item in messages:
        if item.get("type") != "service":
            continue

        action = item.get("action")
        if action == "join_group_by_link":
            telegram_id = parse_user_id(item.get("actor_id"))
            if telegram_id is not None:
                analysis.link_events += 1
                record(telegram_id, parse_export_datetime(item))
            continue

        if action != "invite_members":
            continue

        for member_name in item.get("members") or []:
            analysis.invite_references += 1
            matches = aliases.get(member_name, set())
            if len(matches) == 1:
                analysis.resolved_invites += 1
                record(next(iter(matches)), parse_export_datetime(item))
            elif matches:
                analysis.ambiguous_invites += 1
            else:
                analysis.unmatched_invites += 1

    return analysis


def analyze_telegram_json(path: str | Path) -> dict[str, int]:
    with Path(path).open("r", encoding="utf-8") as file:
        data = json.load(file)

    messages = data.get("messages", [])
    membership = analyze_membership_events(messages)
    return {
        "items": len(messages),
        "messages": sum(item.get("type") == "message" for item in messages),
        "service_messages": sum(
            item.get("type") == "service" for item in messages
        ),
        "link_events": membership.link_events,
        "invite_references": membership.invite_references,
        "resolved_invites": membership.resolved_invites,
        "ambiguous_invites": membership.ambiguous_invites,
        "unmatched_invites": membership.unmatched_invites,
        "users_with_join_date": len(membership.joined_at_by_user),
    }


async def synchronize_user_statistics(session, user_ids: list[int]) -> None:
    if not user_ids:
        return

    statistics = (
        select(
            Message.user_id.label("user_id"),
            func.count(Message.id).label("messages_count"),
            func.count(Message.id)
            .filter(Message.reply_to_message_id.is_not(None))
            .label("replies_count"),
            func.count(Message.id)
            .filter(Message.message_type != "text")
            .label("media_count"),
            func.max(Message.telegram_date).label("last_message_at"),
        )
        .where(Message.user_id.in_(user_ids))
        .group_by(Message.user_id)
        .subquery()
    )
    await session.execute(
        update(User)
        .where(User.id == statistics.c.user_id)
        .values(
            messages_count=statistics.c.messages_count,
            replies_count=statistics.c.replies_count,
            media_count=statistics.c.media_count,
            last_message_at=statistics.c.last_message_at,
            last_activity_at=statistics.c.last_message_at,
        )
    )


async def import_telegram_json(
    path: str | Path,
    session_factory=SessionLocal,
) -> dict[str, int]:
    with Path(path).open("r", encoding="utf-8") as file:
        data = json.load(file)

    all_items = data.get("messages", [])
    users: dict[int, dict] = {}
    source_messages: list[dict] = []

    for item in all_items:
        if item.get("type") != "message":
            continue

        telegram_id = parse_user_id(item.get("from_id"))
        if telegram_id is None:
            continue

        users[telegram_id] = {
            "telegram_id": telegram_id,
            "username": None,
            "first_name": item.get("from"),
            "last_name": None,
        }
        source_messages.append({"item": item, "telegram_id": telegram_id})

    if not users:
        return {"users": 0, "messages": 0}

    chat_id = normalize_export_chat_id(int(data["id"]), data.get("type"))
    chat_title = data.get("name")

    async with session_factory() as session:
        known_aliases: dict[str, set[int]] = {}
        existing_users = (
            await session.execute(
                select(
                    User.telegram_id,
                    User.first_name,
                    User.last_name,
                )
            )
        ).all()
        for telegram_id, first_name, last_name in existing_users:
            display_name = " ".join(
                part for part in (first_name, last_name) if part
            )
            if display_name:
                known_aliases.setdefault(display_name, set()).add(telegram_id)

        membership = analyze_membership_events(all_items, known_aliases)
        user_insert = insert(User).values(list(users.values()))
        user_insert = (
            user_insert.on_conflict_do_nothing(
                index_elements=[User.telegram_id],
            )
            .returning(User.id)
        )
        inserted_users = len((await session.execute(user_insert)).scalars().all())

        known_telegram_ids = set(users) | set(membership.joined_at_by_user)
        user_rows = await session.execute(
            select(User.telegram_id, User.id).where(
                User.telegram_id.in_(known_telegram_ids)
            )
        )
        user_ids = dict(user_rows.all())

        membership_updates = 0
        for telegram_id, joined_at in membership.joined_at_by_user.items():
            user_id = user_ids.get(telegram_id)
            if user_id is None:
                continue
            await session.execute(
                update(User)
                .where(User.id == user_id)
                .values(
                    joined_at=func.least(
                        func.coalesce(User.joined_at, joined_at),
                        joined_at,
                    ),
                    first_seen_at=func.least(
                        func.coalesce(User.first_seen_at, joined_at),
                        joined_at,
                    ),
                )
            )
            membership_updates += 1

        inserted_messages = 0
        telegram_message_ids: list[int] = []

        for start in range(0, len(source_messages), BATCH_SIZE):
            source_batch = source_messages[start : start + BATCH_SIZE]
            values = []

            for source in source_batch:
                item = source["item"]
                telegram_message_id = int(item["id"])
                telegram_message_ids.append(telegram_message_id)
                values.append(
                    {
                        "telegram_message_id": telegram_message_id,
                        "telegram_chat_type": "supergroup",
                        "telegram_chat_title": chat_title,
                        "user_id": user_ids[source["telegram_id"]],
                        "chat_id": chat_id,
                        "message_type": item.get("media_type") or "text",
                        "text": parse_text(item.get("text", "")),
                        "telegram_date": parse_export_datetime(item),
                    }
                )

            existing_message_ids = set(
                (
                    await session.execute(
                        select(Message.telegram_message_id).where(
                            Message.chat_id == chat_id,
                            Message.telegram_message_id.in_(
                                [value["telegram_message_id"] for value in values]
                            ),
                        )
                    )
                ).scalars()
            )
            inserted_messages += len(values) - len(existing_message_ids)

            message_insert = insert(Message).values(values)
            message_insert = message_insert.on_conflict_do_update(
                constraint="uq_messages_chat_message",
                set_={
                    "telegram_chat_title": message_insert.excluded.telegram_chat_title,
                    "user_id": message_insert.excluded.user_id,
                    "message_type": message_insert.excluded.message_type,
                    "text": message_insert.excluded.text,
                    "telegram_date": message_insert.excluded.telegram_date,
                },
            )
            await session.execute(message_insert)

        message_rows = await session.execute(
            select(Message.telegram_message_id, Message.id).where(
                Message.chat_id == chat_id,
                Message.telegram_message_id.in_(telegram_message_ids),
            )
        )
        message_ids = dict(message_rows.all())

        reply_updates = []
        for source in source_messages:
            item = source["item"]
            reply_to = item.get("reply_to_message_id")
            message_id = message_ids.get(int(item["id"]))
            reply_to_id = message_ids.get(int(reply_to)) if reply_to else None

            if message_id is not None and reply_to_id is not None:
                reply_updates.append(
                    {
                        "target_message_id": message_id,
                        "target_reply_id": reply_to_id,
                    }
                )

        if reply_updates:
            await session.execute(
                Message.__table__
                .update()
                .where(Message.id == bindparam("target_message_id"))
                .values(reply_to_message_id=bindparam("target_reply_id")),
                reply_updates,
            )

        await synchronize_user_statistics(
            session,
            [user_ids[telegram_id] for telegram_id in users],
        )

        await session.commit()

    return {
        "users": inserted_users,
        "messages": inserted_messages,
        "membership_dates": membership_updates,
    }
