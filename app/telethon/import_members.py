from telethon.tl.types import User as TelegramUser

from app.telethon.client import client


async def import_members(
    chat_id: int,
):
    await client.start()

    entity = await client.get_entity(chat_id)

    if entity is None:
        raise RuntimeError(
            f"Чат {chat_id} не знайдено."
        )

    print("=" * 60)
    print(entity)
    print(type(entity))
    print("=" * 60)
    print()

    count = 0

    async for member in client.iter_participants(entity):

        member: TelegramUser

        count += 1

        print(
            f"{count:3} | "
            f"{member.id:<12} | "
            f"{member.first_name} "
            f"{member.last_name or ''} "
            f"(@{member.username})"
        )

    print()
    print("=" * 60)
    print(f"Знайдено учасників: {count}")
    print("=" * 60)

    await client.disconnect()