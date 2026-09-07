import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert

from app.database.database import SessionLocal
from app.database.models import Message, User

BATCH_SIZE = 500


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


async def import_telegram_json(path: str | Path) -> dict[str, int]:
    with Path(path).open("r", encoding="utf-8") as file:
        data = json.load(file)

    users: dict[int, dict] = {}
    source_messages: list[dict] = []

    for item in data.get("messages", []):
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

    chat_id = int(data["id"])
    chat_title = data.get("name")

    async with SessionLocal() as session:
        user_insert = insert(User).values(list(users.values()))
        user_insert = (
            user_insert.on_conflict_do_nothing(
                index_elements=[User.telegram_id],
            )
            .returning(User.id)
        )
        inserted_users = len((await session.execute(user_insert)).scalars().all())

        user_rows = await session.execute(
            select(User.telegram_id, User.id).where(User.telegram_id.in_(users))
        )
        user_ids = dict(user_rows.all())

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
                        "telegram_date": datetime.fromisoformat(item["date"]),
                    }
                )

            message_insert = insert(Message).values(values)
            message_insert = message_insert.on_conflict_do_nothing(
                constraint="uq_messages_chat_message"
            )
            message_insert = message_insert.returning(Message.id)
            result = await session.execute(message_insert)
            inserted_messages += len(result.scalars().all())

        message_rows = await session.execute(
            select(Message.telegram_message_id, Message.id).where(
                Message.chat_id == chat_id,
                Message.telegram_message_id.in_(telegram_message_ids),
            )
        )
        message_ids = dict(message_rows.all())

        for source in source_messages:
            item = source["item"]
            reply_to = item.get("reply_to_message_id")
            message_id = message_ids.get(int(item["id"]))
            reply_to_id = message_ids.get(int(reply_to)) if reply_to else None

            if message_id is not None and reply_to_id is not None:
                await session.execute(
                    update(Message)
                    .where(Message.id == message_id)
                    .values(reply_to_message_id=reply_to_id)
                )

        await synchronize_user_statistics(session, list(user_ids.values()))

        await session.commit()

    return {"users": inserted_users, "messages": inserted_messages}
