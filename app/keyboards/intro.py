from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.config import Links


def intro_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👋 Представитися",
                    url=Links.INTRO,
                )
            ]
        ]
    )
