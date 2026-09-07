from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from telethon.tl.custom.message import Message

from app.services.message_processor.dto.telegram_message import (
    TelegramMessageDTO,
)


def get_content_type(message: Any) -> str:
    checks = (
        ("photo", "photo"),
        ("sticker", "sticker"),
        ("video_note", "video_note"),
        ("voice", "voice"),
        ("audio", "audio"),
        ("gif", "animation"),
        ("video", "video"),
        ("document", "document"),
    )
    for attribute, content_type in checks:
        if getattr(message, attribute, None):
            return content_type

    return "text"


def from_telethon(
    message: "Message",
    chat_title: str | None = None,
) -> TelegramMessageDTO:
    content_type = get_content_type(message)

    sender = None

    if message.sender:
        sender = message.sender.id

    sender_chat = None

    if message.sender_id and message.sender_id < 0:
        sender_chat = abs(message.sender_id)

    return TelegramMessageDTO(
        telegram_message_id=message.id,

        chat_id=message.chat_id,
        chat_type="supergroup",
        chat_title=chat_title,
        chat_username=None,

        user_id=sender,

        text=message.text if content_type == "text" else None,
        caption=message.text if content_type != "text" else None,

        content_type=content_type,

        date=message.date,
        edit_date=message.edit_date,

        reply_to_message_id=(
            message.reply_to.reply_to_msg_id
            if message.reply_to
            else None
        ),

        thread_id=getattr(
            message,
            "reply_to_top_id",
            None,
        ),

        media_group_id=(
            str(message.grouped_id)
            if message.grouped_id
            else None
        ),

        sender_chat_id=sender_chat,

        via_bot_id=None,

        entities=message.entities,

        caption_entities=None,

        forward_origin=message.forward,

        external_reply=None,

        quote=None,

        link_preview=None,

        has_media_spoiler=False,

        is_topic_message=False,

        effect_id=None,

        business_connection_id=None,
    )
