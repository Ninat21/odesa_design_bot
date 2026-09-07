from telethon import TelegramClient

from app.config import Config

if Config.API_ID is None or not Config.API_HASH:
    raise RuntimeError("API_ID і API_HASH потрібні для роботи Telethon")


client = TelegramClient(
    "telegram_session",
    Config.API_ID,
    Config.API_HASH,
)
