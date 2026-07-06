from app.services.message_processor.dto.telegram_message import (
    TelegramMessageDTO,
)

from aiogram.types import Message


def from_aiogram(
    message: Message,
) -> TelegramMessageDTO:

    return TelegramMessageDTO(
        telegram_message_id=message.message_id,

        chat_id=message.chat.id,
        chat_type=message.chat.type,
        chat_title=getattr(message.chat, "title", None),
        chat_username=getattr(message.chat, "username", None),

        user_id=(
            message.from_user.id
            if message.from_user
            else None
        ),

        text=message.text,
        caption=message.caption,

        content_type=message.content_type,

        date=message.date,
        edit_date=message.edit_date,

        reply_to_message_id=(
            message.reply_to_message.message_id
            if message.reply_to_message
            else None
        ),

        thread_id=message.message_thread_id,

        media_group_id=message.media_group_id,

        sender_chat_id=(
            message.sender_chat.id
            if message.sender_chat
            else None
        ),

        via_bot_id=(
            message.via_bot.id
            if message.via_bot
            else None
        ),

        entities=message.entities,
        caption_entities=message.caption_entities,

        forward_origin=message.forward_origin,

        external_reply=message.external_reply,

        quote=message.quote,

        link_preview=message.link_preview_options,

        has_media_spoiler=getattr(
            message,
            "has_media_spoiler",
            False,
        ),

        is_topic_message=getattr(
            message,
            "is_topic_message",
            False,
        ),

        effect_id=getattr(
            message,
            "effect_id",
            None,
        ),

        business_connection_id=getattr(
            message,
            "business_connection_id",
            None,
        ),
    )