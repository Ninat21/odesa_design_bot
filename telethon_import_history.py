import asyncio

from app.config import Config
from app.database.database import SessionLocal
from app.database.uow import UnitOfWork
from app.services.factory import ServiceFactory
from app.telethon.client import client

COMMIT_INTERVAL = 100


async def main() -> None:
    await client.start()

    try:
        entity = await client.get_entity(Config.GROUP_ID)
        print(f"Імпорт історії: {entity.title}")

        async with SessionLocal() as session:
            services = ServiceFactory(UnitOfWork(session))
            processed = 0
            failed = 0

            async for message in client.iter_messages(entity, reverse=True):
                try:
                    async with session.begin_nested():
                        result = await services.message_processor.process_telethon(
                            message,
                            chat_title=entity.title,
                        )

                    if result is not None:
                        processed += 1

                    if processed and processed % COMMIT_INTERVAL == 0:
                        await session.commit()
                        print(f"Оброблено {processed}")
                except Exception as error:
                    failed += 1
                    print(
                        f"Помилка в повідомленні {message.id}: "
                        f"{type(error).__name__}: {error}"
                    )

            await session.commit()

        print(f"Готово. Оброблено: {processed}; помилок: {failed}.")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
