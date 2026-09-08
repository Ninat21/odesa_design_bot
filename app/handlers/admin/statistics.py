from html import escape

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.filters.admin import AdminFilter
from app.services.factory import ServiceFactory

router = Router()


def user_link(user):
    if user.username:
        return f"@{escape(user.username)}"

    name = escape(user.first_name or str(user.telegram_id))

    return f'<a href="tg://user?id={user.telegram_id}">{name}</a>'


def membership_date(user):
    return user.joined_at


async def answer_html(message: Message, text: str) -> None:
    chunk = ""

    for line in text.splitlines(keepends=True):
        if chunk and len(chunk) + len(line) > 4_000:
            await message.answer(chunk, parse_mode="HTML")
            chunk = ""
        chunk += line

    if chunk:
        await message.answer(chunk, parse_mode="HTML")


@router.message(Command("top10"), AdminFilter())
async def top10(
    message: Message,
    services: ServiceFactory,
):
    users = await services.statistics.top10()

    text = "🏆 ТОП-10 за весь час\n\n"

    for i, (user, messages) in enumerate(users, start=1):
        text += f"{i}. {user_link(user)} — {messages}\n"

    await answer_html(message, text)


@router.message(Command("top20"), AdminFilter())
async def top20(
    message: Message,
    services: ServiceFactory,
):
    users = await services.statistics.top20()

    text = "🏆 ТОП-20 за весь час\n\n"

    for i, (user, messages) in enumerate(users, start=1):
        text += f"{i}. {user_link(user)} — {messages}\n"

    await answer_html(message, text)


@router.message(Command("top10_90"), AdminFilter())
async def top10_90(
    message: Message,
    services: ServiceFactory,
):
    users = await services.statistics.top10_90()

    text = "🏆 ТОП-10 за останні 90 днів\n\n"

    for i, (user, messages) in enumerate(users, start=1):
        text += f"{i}. {user_link(user)} — {messages}\n"

    await answer_html(message, text)


@router.message(Command("top20_90"), AdminFilter())
async def top20_90(
    message: Message,
    services: ServiceFactory,
):
    users = await services.statistics.top20_90()

    text = "🏆 ТОП-20 за останні 90 днів\n\n"

    for i, (user, messages) in enumerate(users, start=1):
        text += f"{i}. {user_link(user)} — {messages}\n"

    await answer_html(message, text)


@router.message(Command("silent"), AdminFilter())
async def silent(
    message: Message,
    services: ServiceFactory,
):
    users = await services.statistics.users_without_messages()

    text = "🤐 Ніколи не писали:\n\n"

    for i, user in enumerate(users, start=1):
        text += f"{i}. {user_link(user)}\n"

    await answer_html(message, text)


@router.message(Command("one"), AdminFilter())
async def one(
    message: Message,
    services: ServiceFactory,
):
    users = await services.statistics.users_with_one_message()

    text = "1️⃣ Написали лише одне повідомлення:\n\n"

    for i, (user, _) in enumerate(users, start=1):
        text += f"{i}. {user_link(user)}\n"

    await answer_html(message, text)


@router.message(Command("inactive30"), AdminFilter())
async def inactive30(
    message: Message,
    services: ServiceFactory,
):
    users = await services.statistics.inactive30()

    text = "😴 Не писали 30 днів:\n\n"

    for i, (user, messages, last_message) in enumerate(users, start=1):
        date = last_message.strftime("%d.%m.%Y")

        text += f"{i}. {user_link(user)} ({messages} повідомлень, останнє {date})\n"

    await answer_html(message, text)


@router.message(Command("inactive90"), AdminFilter())
async def inactive90(
    message: Message,
    services: ServiceFactory,
):
    users = await services.statistics.inactive90()

    text = "💤 Не писали 90 днів:\n\n"

    for i, (user, messages, last_message) in enumerate(users, start=1):
        date = last_message.strftime("%d.%m.%Y")

        text += f"{i}. {user_link(user)} ({messages} повідомлень, останнє {date})\n"

    await answer_html(message, text)


@router.message(Command("oldest20"), AdminFilter())
async def oldest20(
    message: Message,
    services: ServiceFactory,
):
    users = await services.statistics.oldest20()

    text = "🏛 20 найстаріших учасників:\n\n"

    for i, user in enumerate(users, start=1):
        date = membership_date(user).strftime("%d.%m.%Y")

        text += f"{i}. {user_link(user)} ({date})\n"

    await answer_html(message, text)


@router.message(Command("oldest50"), AdminFilter())
async def oldest50(
    message: Message,
    services: ServiceFactory,
):
    users = await services.statistics.oldest50()

    text = "🏛 50 найстаріших учасників:\n\n"

    for i, user in enumerate(users, start=1):
        date = membership_date(user).strftime("%d.%m.%Y")

        text += f"{i}. {user_link(user)} ({date})\n"

    await answer_html(message, text)


@router.message(Command("new30"), AdminFilter())
async def new30(
    message: Message,
    services: ServiceFactory,
):
    users = await services.statistics.new30()

    text = "🆕 Нові учасники за 30 днів:\n\n"

    for i, user in enumerate(users, start=1):
        date = membership_date(user).strftime("%d.%m.%Y")

        text += f"{i}. {user_link(user)} ({date})\n"

    await answer_html(message, text)
