from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError

from app.database.crud import get_stats
from app.filters.admin import AdminFilter

router = Router()


@router.message(Command("stats"), AdminFilter())
async def stats(message: Message):

    users, messages = get_stats()

    text = f"""
📊 <b>Статистика спільноти</b>

👥 Користувачів: <b>{users}</b>
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