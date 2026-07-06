from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def welcome_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👋 Знайомство", url="")],
            [InlineKeyboardButton(text="📅 Події", url="")],
            [InlineKeyboardButton(text="💼 Попрацюємо?", url="")],
        ]
    )

    return keyboard
