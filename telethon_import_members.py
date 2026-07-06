import asyncio

from app.telethon.import_members import import_members


CHAT_ID = -1002511970112


asyncio.run(
    import_members(CHAT_ID)
)