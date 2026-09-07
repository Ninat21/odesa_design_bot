from time import monotonic

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

START_TIME = monotonic()


@router.message(Command("ping"))
async def ping(
    message: Message,
):
    uptime_seconds = int(monotonic() - START_TIME)

    hours, remainder = divmod(
        uptime_seconds,
        3600,
    )

    minutes, seconds = divmod(
        remainder,
        60,
    )

    await message.answer(
        f"✅ Бот працює\n\nТривалість роботи: {hours} год {minutes} хв {seconds} сек"
    )
