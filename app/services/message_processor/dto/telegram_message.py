from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class TelegramMessageDTO:

    telegram_message_id: int

    chat_id: int
    chat_type: str
    chat_title: str | None
    chat_username: str | None

    user_id: int | None

    text: str | None
    caption: str | None

    content_type: str

    date: datetime
    edit_date: datetime | None

    reply_to_message_id: int | None

    thread_id: int | None

    media_group_id: str | None

    sender_chat_id: int | None

    via_bot_id: int | None

    entities: Any
    caption_entities: Any

    forward_origin: Any

    external_reply: Any

    quote: Any

    link_preview: Any

    has_media_spoiler: bool

    is_topic_message: bool

    effect_id: str | None

    business_connection_id: str | None