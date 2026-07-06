from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.factory import ServiceFactory

router = Router()

START_TIME = datetime.now()


@router.message(Command("ping"))
async def ping(
    message: Message,
    services: ServiceFactory,
):
    await services.message_processor.process(
        telegram_user=message.from_user,
        telegram_message=message,
    )

    uptime = datetime.now() - START_TIME

    hours, remainder = divmod(
        int(uptime.total_seconds()),
        3600,
    )

    minutes, seconds = divmod(
        remainder,
        60,
    )

    await message.answer(
        f"✅ Бот працює\n\n"
        f"Тривалість роботи: "
        f"{hours} год {minutes} хв {seconds} сек"
    )