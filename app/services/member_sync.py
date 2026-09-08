from datetime import UTC, datetime

from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy import select

from app.database.database import SessionLocal
from app.database.models import User
from app.database.repositories.users import UserRepository
from app.services.message_processor.steps.save_user import SaveUserStep


def is_current_member(chat_member) -> bool:
    if chat_member.status in {
        ChatMemberStatus.CREATOR,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.MEMBER,
    }:
        return True
    return (
        chat_member.status == ChatMemberStatus.RESTRICTED
        and chat_member.is_member
    )


async def synchronize_known_members(
    bot,
    chat_id: int,
    session_factory=SessionLocal,
) -> dict[str, int]:
    counts = {"members": 0, "left": 0, "unavailable": 0}
    observed_at = datetime.now(UTC)

    async with session_factory() as session:
        telegram_ids = list(
            await session.scalars(select(User.telegram_id).order_by(User.id))
        )
        users = UserRepository(session)
        save_user = SaveUserStep(users)

        for telegram_id in telegram_ids:
            try:
                chat_member = await bot.get_chat_member(chat_id, telegram_id)
            except TelegramBadRequest:
                counts["unavailable"] += 1
                continue

            user = await save_user.execute(chat_member.user)
            if is_current_member(chat_member):
                await users.mark_present(user, observed_at)
                counts["members"] += 1
            else:
                if user.is_member:
                    await users.mark_left(user, observed_at)
                counts["left"] += 1

        await session.commit()

    return counts
