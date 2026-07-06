from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.config import Links


def start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📖 Познайомитися зі спільнотою",
                    url=Links.ABOUT,
                )
            ]
        ]
    )
