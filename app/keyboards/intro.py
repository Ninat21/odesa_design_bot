from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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