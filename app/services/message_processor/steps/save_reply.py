from aiogram.types import Message as TelegramMessage

from app.database.repositories.messages import MessageRepository


class SaveReplyStep:
    def __init__(
        self,
        messages: MessageRepository,
    ):
        self.messages = messages

    async def execute(
        self,
        telegram_message: TelegramMessage,
    ) -> int | None:

        if telegram_message.reply_to_message is None:
            return None

        reply = await self.messages.get_by_telegram_message_id(
            chat_id=telegram_message.chat.id,
            telegram_message_id=telegram_message.reply_to_message.message_id,
        )

        if reply is None:
            return None

        return reply.id