from datetime import UTC, datetime

from sqlalchemy import select

from app.database.database import SessionLocal
from app.database.models import User
from app.database.repositories.users import UserRepository
from app.services.message_processor.steps.save_user import SaveUserStep
from app.telethon.client import client


async def import_members(
    chat_id: int,
    telegram_client=client,
    session_factory=SessionLocal,
) -> dict[str, int]:
    await telegram_client.start()

    try:
        entity = await telegram_client.get_entity(chat_id)

        if entity is None:
            raise RuntimeError(f"Чат {chat_id} не знайдено.")

        participants = await telegram_client.get_participants(entity, limit=0)
        expected_count = participants.total
        observed_at = datetime.now(UTC)
        seen_ids: set[int] = set()

        async with session_factory() as session:
            users = UserRepository(session)
            save_user = SaveUserStep(users)
            existing_ids = set(await session.scalars(select(User.telegram_id)))

            async for member in telegram_client.iter_participants(entity):
                seen_ids.add(member.id)
                user = await save_user.execute_telethon(member)
                participant = getattr(member, "participant", None)
                joined_at = getattr(participant, "date", None)
                if joined_at is not None:
                    await users.mark_joined(user, joined_at)
                await users.mark_present(user, observed_at)

            if len(seen_ids) != expected_count:
                raise RuntimeError(
                    "Telegram повернув неповний список учасників: "
                    f"очікувалося {expected_count}, отримано {len(seen_ids)}. "
                    "Статуси користувачів не змінено."
                )

            users_who_left = list(
                await session.scalars(
                    select(User).where(
                        User.is_member.is_(True),
                        User.telegram_id.not_in(seen_ids),
                    )
                )
            )
            for user in users_who_left:
                await users.mark_left(user, observed_at)

            await session.commit()

        result = {
            "members": len(seen_ids),
            "added": len(seen_ids - existing_ids),
            "updated": len(seen_ids & existing_ids),
            "left": len(users_who_left),
        }
        print(f"Синхронізацію завершено: {result}")
        return result
    finally:
        await telegram_client.disconnect()
