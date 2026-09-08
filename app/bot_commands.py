from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    BotCommand,
    BotCommandScopeChat,
    BotCommandScopeChatMember,
    BotCommandScopeDefault,
    MenuButtonCommands,
)

from app.config import Config
from app.core.logger import logger

PUBLIC_COMMANDS = (
    ("help", "Показати всі доступні команди"),
    ("setup", "Про спільноту та корисні посилання"),
    ("ping", "Перевірити, чи працює бот"),
)

ADMIN_COMMANDS = (
    ("stats", "Загальна статистика спільноти"),
    ("members", "Клікабельний список усіх учасників"),
    ("inactive3m", "Не писали останні три місяці"),
    ("top10", "10 найактивніших за весь час"),
    ("top20", "20 найактивніших за весь час"),
    ("top10_90", "10 найактивніших за 90 днів"),
    ("top20_90", "20 найактивніших за 90 днів"),
    ("silent", "Учасники, які ніколи не писали"),
    ("one", "Учасники з одним повідомленням"),
    ("inactive30", "Не писали понад 30 днів"),
    ("inactive90", "Не писали понад 90 днів"),
    ("oldest20", "20 найдавніших учасників"),
    ("oldest50", "50 найдавніших учасників"),
    ("new30", "Нові учасники за 30 днів"),
)


def as_bot_commands(commands) -> list[BotCommand]:
    return [
        BotCommand(command=command, description=description)
        for command, description in commands
    ]


def command_help_text(is_admin: bool) -> str:
    commands = PUBLIC_COMMANDS + (ADMIN_COMMANDS if is_admin else ())
    heading = "📋 Доступні команди"
    if is_admin:
        heading += " (включно з командами адміністратора)"

    lines = [heading, ""]
    lines.extend(
        f"/{command} — {description}" for command, description in commands
    )
    return "\n".join(lines)


async def setup_bot_commands(bot: Bot) -> None:
    public = as_bot_commands(PUBLIC_COMMANDS)
    admin = as_bot_commands(PUBLIC_COMMANDS + ADMIN_COMMANDS)

    await bot.set_my_commands(public, scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

    for admin_id in Config.ADMIN_IDS:
        scopes = (
            BotCommandScopeChat(chat_id=admin_id),
            BotCommandScopeChatMember(
                chat_id=Config.GROUP_ID,
                user_id=admin_id,
            ),
        )
        for scope in scopes:
            try:
                await bot.set_my_commands(admin, scope=scope)
            except TelegramBadRequest as error:
                logger.warning(
                    "Не вдалося налаштувати меню команд для адміністратора %s: %s",
                    admin_id,
                    error,
                )
