import asyncio

from app.database.database import SessionLocal
from app.database.uow import UnitOfWork
from app.services.factory import ServiceFactory
from app.telethon.client import client


CHAT_ID = -1002511970112


async def main():

    await client.start()

    entity = await client.get_entity(CHAT_ID)

    print(f"Імпорт історії: {entity.title}")
    print()

    async with SessionLocal() as session:

        uow = UnitOfWork(session)
        services = ServiceFactory(uow)

        imported = 0

        async for message in client.iter_messages(
            entity,
            reverse=True,
        ):

            try:

                await services.message_processor.process_telethon(
                    message,
                    chat_title=entity.title,
                )

                imported += 1

                if imported % 100 == 0:
                    print(f"Імпортовано {imported}")

            except Exception as e:

                print(f"\nПомилка в повідомленні {message.id}")
                print(type(e).__name__)
                print(e)

        await session.commit()

    await client.disconnect()

    print()
    print("=" * 60)
    print(f"Готово. Імпортовано {imported} повідомлень.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())