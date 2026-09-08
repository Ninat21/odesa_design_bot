from aiogram import Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command
from aiogram.types import Message

from app.filters.admin import AdminFilter
from app.services.factory import ServiceFactory

router = Router()


@router.message(Command("stats"), AdminFilter())
async def stats(
    message: Message,
    services: ServiceFactory,
) -> None:
    current_users, left_users, messages = await services.statistics.totals()

    text = f"""
📊 <b>Статистика спільноти</b>

👥 Учасників зараз: <b>{current_users}</b>
🚪 Вийшли або більше не в групі: <b>{left_users}</b>
📋 Всього відомих людей: <b>{current_users + left_users}</b>
💬 Повідомлень: <b>{messages}</b>
"""

    try:
        await message.bot.send_message(
            chat_id=message.from_user.id,
            text=text,
        )

        if message.chat.type != "private":
            await message.delete()
    except TelegramForbiddenError:
        await message.reply(
            "❗️Спочатку відкрийте особистий чат із ботом і натисніть /start."
        )
