from typing import TYPE_CHECKING

from aiogram.types import Message as TelegramMessage
from aiogram.types import User as TelegramUser

if TYPE_CHECKING:
    from telethon.tl.custom.message import Message as TelethonMessage

from app.database.models import Message
from app.services.attachment_service import AttachmentService
from app.services.message_processor.dto.from_aiogram import from_aiogram
from app.services.message_processor.dto.from_telethon import (
    from_telethon,
)

from .steps.save_message import SaveMessageStep
from .steps.save_reply import SaveReplyStep
from .steps.save_user import SaveUserStep


class MessageProcessor:
    def __init__(
        self,
        save_user: SaveUserStep,
        save_reply: SaveReplyStep,
        save_message: SaveMessageStep,
        attachment_service: AttachmentService,
    ):
        self.save_user = save_user
        self.save_reply = save_reply
        self.save_message = save_message
        self.attachment_service = attachment_service

    async def process_telethon(
        self,
        telegram_message: "TelethonMessage",
        chat_title: str | None = None,
    ) -> Message | None:

        dto = from_telethon(
            telegram_message,
            chat_title=chat_title,
        )

        sender = await telegram_message.get_sender()

        if sender is None:
            return None

        user = await self.save_user.execute_telethon(
            sender,
        )

        reply_to_message_id = None
        if dto.reply_to_message_id is not None:
            reply_to_message_id = await self.save_reply.resolve(
                chat_id=dto.chat_id,
                telegram_message_id=dto.reply_to_message_id,
            )

        message = await self.save_message.execute(
            message=dto,
            user=user,
            reply_to_message_id=reply_to_message_id,
        )

        return message

    async def process(
        self,
        telegram_user: TelegramUser,
        telegram_message: TelegramMessage,
    ) -> Message:

        dto = from_aiogram(
            telegram_message,
        )

        user = await self.save_user.execute_member(
            telegram_user,
            telegram_message.date,
        )

        reply_to_message_id = await self.save_reply.execute(
            telegram_message,
        )

        message = await self.save_message.execute(
            message=dto,
            user=user,
            reply_to_message_id=reply_to_message_id,
        )

        await self.attachment_service.save_attachments(
            telegram_message,
            message,
        )

        return message
