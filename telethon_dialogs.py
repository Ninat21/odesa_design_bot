import asyncio

from app.telethon.client import client


async def main():
    await client.start()

    try:
        print()

        async for dialog in client.iter_dialogs():
            print(f"{dialog.id:<15} | {dialog.name}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
