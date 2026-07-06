import json

from app.database.models import Message
from app.database.models import User
from app.database.repositories.messages import MessageRepository
from app.services.message_processor.dto.telegram_message import (
    TelegramMessageDTO,
)


class SaveMessageStep:
    def __init__(
        self,
        messages: MessageRepository,
    ):
        self.messages = messages

    async def execute(
        self,
        message: TelegramMessageDTO,
        user: User,
        reply_to_message_id: int | None = None,
    ) -> Message:

        db_message = await self.messages.get_by_telegram_message_id(
            chat_id=message.chat_id,
            telegram_message_id=message.telegram_message_id,
        )

        if db_message:
            return db_message

        return await self.messages.create(
            telegram_message_id=message.telegram_message_id,

            telegram_chat_type=message.chat_type,
            telegram_chat_title=message.chat_title,
            telegram_chat_username=message.chat_username,

            user_id=user.id,

            chat_id=message.chat_id,
            thread_id=message.thread_id,
            media_group_id=message.media_group_id,

            reply_to_message_id=reply_to_message_id,

            sender_chat_id=message.sender_chat_id,
            via_bot_id=message.via_bot_id,

            message_type=message.content_type,

            text=message.text,
            caption=message.caption,

            entities_json=self._to_json(
                message.entities,
            ),

            caption_entities_json=self._to_json(
                message.caption_entities,
            ),

            forward_origin_json=self._to_json(
                message.forward_origin,
            ),

            external_reply_json=self._to_json(
                message.external_reply,
            ),

            quote_json=self._to_json(
                message.quote,
            ),

            link_preview_json=self._to_json(
                message.link_preview,
            ),

            telegram_date=message.date,
            edited_at=message.edit_date,

            has_media_spoiler=message.has_media_spoiler,
            is_topic_message=message.is_topic_message,

            effect_id=message.effect_id,
            business_connection_id=message.business_connection_id,
        )

    def _to_json(
        self,
        obj,
    ) -> str | None:

        if obj is None:
            return None

        if isinstance(obj, list):

            result = []

            for item in obj:

                if hasattr(item, "model_dump"):
                    result.append(item.model_dump())

                elif hasattr(item, "to_dict"):
                    result.append(item.to_dict())

                else:
                    result.append(str(item))

            return json.dumps(
                result,
                ensure_ascii=False,
            )

        if hasattr(obj, "model_dump"):

            return json.dumps(
                obj.model_dump(),
                ensure_ascii=False,
            )

        if hasattr(obj, "to_dict"):

            return json.dumps(
                obj.to_dict(),
                ensure_ascii=False,
            )

        return json.dumps(
            str(obj),
            ensure_ascii=False,
        )