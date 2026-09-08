from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.bot_commands import command_help_text
from app.config import Config

router = Router()


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else None
    await message.answer(command_help_text(user_id in Config.ADMIN_IDS))
