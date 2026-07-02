from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def welcome_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👋 Знайомство",
                    url=""
                )
            ],
            [
                InlineKeyboardButton(
                    text="📅 Події",
                    url=""
                )
            ],
            [
                InlineKeyboardButton(
                    text="💼 Попрацюємо?",
                    url=""
                )
            ]
        ]
    )

    return keyboard