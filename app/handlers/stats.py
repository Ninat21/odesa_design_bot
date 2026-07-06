from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command
from aiogram.types import Message

from app.database.models import Message as DBMessage
from app.database.models import User
from app.filters.admin import AdminFilter

router = Router()


@router.message(Command("stats"), AdminFilter())
async def stats(
    message: Message,
    session: AsyncSession,
):
    users = await session.scalar(
        select(func.count(User.id))
    )

    messages = await session.scalar(
        select(func.count(DBMessage.id))
    )

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