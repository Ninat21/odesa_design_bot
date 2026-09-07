from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.filters.chat_member_updated import IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated

from app.keyboards.start import start_keyboard
from app.services.factory import ServiceFactory
from app.texts.welcome import WELCOME_TEXT

router = Router()


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def welcome_new_member(
    event: ChatMemberUpdated,
    services: ServiceFactory,
):
    user = event.new_chat_member.user
    await services.membership.join(user, event.date)
    await services.uow.session.commit()

    await event.bot.send_message(
        chat_id=event.chat.id,
        text=WELCOME_TEXT.format(name=user.mention_html()),
        reply_markup=start_keyboard(),
    )


@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def member_left(
    event: ChatMemberUpdated,
    services: ServiceFactory,
):
    await services.membership.leave(
        event.old_chat_member.user,
        event.date,
    )
