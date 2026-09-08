from html import escape

from aiogram import Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from aiogram.types import Message

from app.filters.admin import AdminFilter
from app.handlers.admin.statistics import member_name_link
from app.services.factory import ServiceFactory

router = Router()

FACT_LABELS = {
    "profession": "Професія",
    "position": "Посада",
    "company": "Компанія",
    "skill": "Навичка",
    "interest": "Інтерес",
    "hobby": "Хобі",
    "birthday": "День народження",
    "age": "Вік",
    "full_name": "Повне ім'я",
    "social": "Соцмережа",
    "portfolio": "Портфоліо",
    "website": "Сайт",
    "bio": "Про себе",
}


def telegram_message_url(message) -> str | None:
    if message is None or message.chat_id >= 0:
        return None
    chat_id = str(abs(message.chat_id))
    if not chat_id.startswith("100"):
        return None
    return f"https://t.me/c/{chat_id[3:]}/{message.telegram_message_id}"


def linked_value(value: str, url: str | None) -> str:
    safe_value = escape(value)
    if not url:
        return safe_value
    return f'<a href="{escape(url, quote=True)}">{safe_value}</a>'


def render_profile_card(user, profile, facts) -> str:
    membership = "у групі" if user.is_member else "більше не в групі"
    lines = [
        f"👤 <b>{member_name_link(user)}</b>",
        f"Статус: {membership}",
    ]
    if user.username:
        lines.append(f"Telegram: @{escape(user.username)}")

    if profile is not None:
        primary_fields = (
            ("Професія", profile.profession),
            ("Посада", profile.position),
            ("Компанія", profile.company),
            ("Місто", profile.city),
            ("Про себе", profile.bio),
        )
        for label, value in primary_fields:
            if value:
                lines.append(f"{label}: {escape(str(value))}")

        links = (
            ("Instagram", profile.instagram),
            ("Behance", profile.behance),
            ("LinkedIn", profile.linkedin),
            ("Портфоліо", profile.portfolio_url),
            ("Сайт", profile.website),
        )
        for label, url in links:
            if url:
                safe_url = escape(url, quote=True)
                lines.append(f'{label}: <a href="{safe_url}">посилання</a>')

    if facts:
        lines.extend(["", "<b>Знайдені факти</b>"])
        for fact, source_message in facts:
            label = FACT_LABELS.get(fact.fact_type, fact.fact_type)
            source_url = telegram_message_url(source_message)
            marker = "✅" if fact.verified else "📝"
            if fact.inferred:
                marker = "🧠"
            confidence = ""
            if fact.confidence is not None:
                confidence = f" · {float(fact.confidence):.0%}"
            lines.append(
                f"{marker} <b>{escape(label)}:</b> "
                f"{linked_value(fact.value, source_url)}{confidence}"
            )
        lines.extend(
            [
                "",
                "✅ підтверджено · 📝 явна згадка · 🧠 припущення",
            ]
        )
    else:
        lines.extend(["", "Поки що факти про користувача не знайдені."])

    return "\n".join(lines)


async def resolve_user(message, command: CommandObject, services: ServiceFactory):
    argument = (command.args or "").strip().split(maxsplit=1)[0]
    if argument:
        if argument.removeprefix("@").isdigit():
            return await services.users.get_by_telegram_id(
                int(argument.removeprefix("@"))
            )
        return await services.users.get_by_username(argument)
    if message.reply_to_message and message.reply_to_message.from_user:
        return await services.users.get_by_telegram_id(
            message.reply_to_message.from_user.id
        )
    if message.from_user:
        return await services.users.get_by_telegram_id(message.from_user.id)
    return None


@router.message(Command("profile"), AdminFilter())
async def profile_card(
    message: Message,
    command: CommandObject,
    services: ServiceFactory,
) -> None:
    user = await resolve_user(message, command, services)
    if user is None:
        await message.reply(
            "Користувача не знайдено. Вкажіть команду як /profile @username "
            "або дайте нею відповідь на повідомлення користувача."
        )
        return

    profile, facts = await services.profiles.get_card(user.id)
    text = render_profile_card(user, profile, facts)

    try:
        await message.bot.send_message(
            chat_id=message.from_user.id,
            text=text,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        if message.chat.type != "private":
            await message.delete()
    except TelegramForbiddenError:
        await message.reply(
            "Спочатку відкрийте особистий чат із ботом і натисніть /start."
        )
