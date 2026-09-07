import asyncio

from app.config import Config
from app.telethon.import_members import import_members

asyncio.run(import_members(Config.GROUP_ID))
