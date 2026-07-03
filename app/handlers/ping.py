from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

START_TIME = datetime.now()


@router.message(Command("ping"))
async def ping(message: Message):
    uptime = datetime.now() - START_TIME

    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)

    await message.answer(
        "✅ Бот працює\n\n"
        f"Тривалість роботи: {hours} ч {minutes} мин {seconds} сек"
    )