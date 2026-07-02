from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from app.texts.intro import get_intro_text

from app.keyboards.intro import intro_keyboard

router = Router()


@router.message(Command("setup"))
async def setup(message: Message):
    
    await message.answer(
        get_intro_text(),
        reply_markup=intro_keyboard()
    )

  