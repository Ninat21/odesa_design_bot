from datetime import datetime, timezone

from app.database.repositories.messages import MessageRepository
from app.database.repositories.users import UserRepository


class MessageService:
    def __init__(
        self,
        users: UserRepository,
        messages: MessageRepository,
        attachment_service,
    ):
        self.users = users
        self.messages = messages
        self.attachment_service = attachment_service

    async def save_message(
        self,
        telegram_user,
        telegram_message,
    ):
        user = await self.users.get_by_telegram_id(
            telegram_user.id
        )

        if user is None:
            user = await self.users.create(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
                language_code=telegram_user.language_code,
                is_bot=telegram_user.is_bot,
                is_premium=getattr(
                    telegram_user,
                    "is_premium",
                    False,
                ),
                first_seen_at=datetime.now(timezone.utc),
                joined_at=datetime.now(timezone.utc),
                last_seen_at=datetime.now(timezone.utc),
                last_activity_at=datetime.now(timezone.utc),
                last_message_at=datetime.now(timezone.utc),
                messages_count=1,
            )
        else:
            user.last_seen_at = datetime.now(timezone.utc)
            user.last_activity_at = datetime.now(timezone.utc)
            user.last_message_at = datetime.now(timezone.utc)
            user.messages_count += 1

            await self.users.save(user)

        reply_to_id = None

        if telegram_message.reply_to_message:
            reply = await self.messages.get_by_telegram_message_id(
                chat_id=telegram_message.chat.id,
                telegram_message_id=telegram_message.reply_to_message.message_id,
            )

            if reply:
                reply_to_id = reply.id

        db_message = await self.messages.create(
            user_id=user.id,
            chat_id=telegram_message.chat.id,
            telegram_message_id=telegram_message.message_id,
            telegram_date=telegram_message.date,
            thread_id=telegram_message.message_thread_id,
            reply_to_message_id=reply_to_id,
            message_type=telegram_message.content_type,
            text=telegram_message.text,
            caption=telegram_message.caption,
        )

        await self.attachment_service.save_attachments(
            telegram_message,
            db_message,
        )

        return db_message