from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.filters.chat_member_updated import IS_NOT_MEMBER, MEMBER
from aiogram.types import ChatMemberUpdated

from app.texts.welcome import WELCOME_TEXT

router = Router()


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> MEMBER))
async def welcome_new_member(event: ChatMemberUpdated):
    print("NEW MEMBER EVENT")

    user = event.new_chat_member.user

    await event.bot.send_message(
        chat_id=event.chat.id,
        text=WELCOME_TEXT.format(name=user.mention_html()),
    )