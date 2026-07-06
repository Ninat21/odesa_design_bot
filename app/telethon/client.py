from telethon import TelegramClient

from app.config import Config


client = TelegramClient(
    "telegram_session",
    Config.API_ID,
    Config.API_HASH,
)