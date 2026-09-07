import asyncio

from app.telethon.auth import authorize

if __name__ == "__main__":
    asyncio.run(authorize())
