from datetime import UTC, datetime

from app.database.database import SessionLocal
from app.database.repositories.users import UserRepository
from app.services.message_processor.steps.save_user import SaveUserStep
from app.telethon.client import client

COMMIT_INTERVAL = 100


async def import_members(
    chat_id: int,
) -> int:
    await client.start()

    try:
        entity = await client.get_entity(chat_id)

        if entity is None:
            raise RuntimeError(f"Чат {chat_id} не знайдено.")

        count = 0
        observed_at = datetime.now(UTC)

        async with SessionLocal() as session:
            save_user = SaveUserStep(UserRepository(session))

            async for member in client.iter_participants(entity):
                user = await save_user.execute_telethon(member)
                await save_user.users.mark_present(user, observed_at)
                count += 1

                if count % COMMIT_INTERVAL == 0:
                    await session.commit()
                    print(f"Збережено учасників: {count}")

            await session.commit()

        print(f"Імпорт завершено. Збережено учасників: {count}")
        return count
    finally:
        await client.disconnect()
