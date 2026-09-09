from html import escape

from aiogram import F, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from app.config import Config
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


class ProfileEdit(StatesGroup):
    waiting_value = State()


def telegram_message_url(message) -> str | None:
    if message is None or message.chat_id >= 0:
        return None
    chat_id = str(abs(message.chat_id))
    if not chat_id.startswith("100"):
        return None
    return f"https://t.me/c/{chat_id[3:]}/{message.telegram_message_id}"


def linked_value(value: str, url: str | None) -> str:
    display_value = value if len(value) <= 350 else f"{value[:347]}..."
    safe_value = escape(display_value)
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
        for number, (fact, source_message) in enumerate(facts, start=1):
            label = FACT_LABELS.get(fact.fact_type, fact.fact_type)
            source_url = telegram_message_url(source_message)
            marker = "✅" if fact.verified else "📝"
            if fact.inferred:
                marker = "🧠"
            confidence = ""
            if fact.confidence is not None:
                confidence = f" · {float(fact.confidence):.0%}"
            lines.append(
                f"{number}. {marker} <b>{escape(label)}:</b> "
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


def profile_fact_keyboard(facts) -> InlineKeyboardMarkup | None:
    rows = []
    for number, (fact, _) in enumerate(facts, start=1):
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"✅ {number}",
                    callback_data=f"pf:verify:{fact.id}",
                ),
                InlineKeyboardButton(
                    text=f"✏️ {number}",
                    callback_data=f"pf:edit:{fact.id}",
                ),
                InlineKeyboardButton(
                    text=f"🗑 {number}",
                    callback_data=f"pf:delete:{fact.id}",
                ),
            ]
        )
    if not rows:
        return None
    return InlineKeyboardMarkup(inline_keyboard=rows)


def is_admin_callback(callback: CallbackQuery) -> bool:
    return callback.from_user.id in Config.ADMIN_IDS


def callback_fact_id(callback: CallbackQuery) -> int | None:
    try:
        return int((callback.data or "").rsplit(":", maxsplit=1)[1])
    except (IndexError, ValueError):
        return None


async def load_fact(callback: CallbackQuery, services: ServiceFactory):
    if not is_admin_callback(callback):
        await callback.answer("Недостатньо прав", show_alert=True)
        return None
    fact_id = callback_fact_id(callback)
    fact = await services.profiles.get_fact(fact_id) if fact_id else None
    if fact is None:
        await callback.answer("Цей факт уже не існує", show_alert=True)
    return fact


async def refresh_callback_card(
    callback: CallbackQuery,
    services: ServiceFactory,
    user_id: int,
) -> None:
    user = await services.users.get_by_id(user_id)
    if user is None or callback.message is None:
        return
    profile, facts = await services.profiles.get_card(user.id)
    await callback.message.edit_text(
        render_profile_card(user, profile, facts),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=profile_fact_keyboard(facts),
    )


async def send_profile_card(
    message: Message,
    services: ServiceFactory,
    user_id: int,
) -> None:
    user = await services.users.get_by_id(user_id)
    if user is None:
        await message.answer("Користувача більше немає в базі.")
        return
    profile, facts = await services.profiles.get_card(user.id)
    await message.answer(
        render_profile_card(user, profile, facts),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=profile_fact_keyboard(facts),
    )


async def resolve_user(message, command: CommandObject, services: ServiceFactory):
    raw_argument = (command.args or "").strip()
    argument = raw_argument.split(maxsplit=1)[0] if raw_argument else ""
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
            reply_markup=profile_fact_keyboard(facts),
        )
        if message.chat.type != "private":
            await message.delete()
    except TelegramForbiddenError:
        await message.reply(
            "Спочатку відкрийте особистий чат із ботом і натисніть /start."
        )


@router.callback_query(F.data.startswith("pf:verify:"))
async def verify_profile_fact(
    callback: CallbackQuery,
    services: ServiceFactory,
) -> None:
    fact = await load_fact(callback, services)
    if fact is None:
        return
    user_id = fact.user_id
    await services.profiles.verify_fact(fact)
    await refresh_callback_card(callback, services, user_id)
    await callback.answer("Факт підтверджено")


@router.callback_query(F.data.startswith("pf:delete:"))
async def request_profile_fact_delete(
    callback: CallbackQuery,
    services: ServiceFactory,
) -> None:
    fact = await load_fact(callback, services)
    if fact is None:
        return
    if callback.message is not None:
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Так, видалити",
                            callback_data=f"pf:destroy:{fact.id}",
                        ),
                        InlineKeyboardButton(
                            text="Скасувати",
                            callback_data=f"pf:cancel:{fact.id}",
                        ),
                    ]
                ]
            )
        )
    await callback.answer("Підтвердьте видалення")


@router.callback_query(F.data.startswith("pf:destroy:"))
async def delete_profile_fact(
    callback: CallbackQuery,
    services: ServiceFactory,
) -> None:
    fact = await load_fact(callback, services)
    if fact is None:
        return
    user_id = fact.user_id
    await services.profiles.delete_fact(fact)
    await refresh_callback_card(callback, services, user_id)
    await callback.answer("Факт видалено")


@router.callback_query(F.data.startswith("pf:cancel:"))
async def cancel_profile_fact_delete(
    callback: CallbackQuery,
    services: ServiceFactory,
) -> None:
    fact = await load_fact(callback, services)
    if fact is None:
        return
    await refresh_callback_card(callback, services, fact.user_id)
    await callback.answer("Видалення скасовано")


@router.callback_query(F.data.startswith("pf:edit:"))
async def start_profile_fact_edit(
    callback: CallbackQuery,
    services: ServiceFactory,
    state: FSMContext,
) -> None:
    fact = await load_fact(callback, services)
    if fact is None:
        return
    await state.set_state(ProfileEdit.waiting_value)
    await state.update_data(fact_id=fact.id, user_id=fact.user_id)
    if callback.message is not None:
        label = FACT_LABELS.get(fact.fact_type, fact.fact_type)
        await callback.message.answer(
            f"Надішліть нове значення для «{label}».\n"
            "Для скасування: /cancel"
        )
    await callback.answer()


@router.message(ProfileEdit.waiting_value, Command("cancel"), AdminFilter())
async def cancel_profile_fact_edit(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Редагування скасовано.")


@router.message(ProfileEdit.waiting_value, AdminFilter())
async def finish_profile_fact_edit(
    message: Message,
    services: ServiceFactory,
    state: FSMContext,
) -> None:
    value = (message.text or "").strip()
    if not value:
        await message.answer("Надішліть нове значення текстом або введіть /cancel.")
        return

    data = await state.get_data()
    fact = await services.profiles.get_fact(data.get("fact_id"))
    if fact is None:
        await state.clear()
        await message.answer("Цей факт уже видалено.")
        return

    user_id = fact.user_id
    await services.profiles.update_fact_value(fact, value)
    await state.clear()
    await message.answer("Факт оновлено і підтверджено.")
    await send_profile_card(message, services, user_id)
