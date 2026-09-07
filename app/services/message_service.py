from app.database.repositories.messages import MessageRepository
from app.database.repositories.users import UserRepository
from app.services.attachment_service import AttachmentService
from app.services.message_processor.processor import MessageProcessor
from app.services.message_processor.steps.save_message import SaveMessageStep
from app.services.message_processor.steps.save_reply import SaveReplyStep
from app.services.message_processor.steps.save_user import SaveUserStep


class MessageService:
    """Compatibility facade for the single canonical message pipeline."""

    def __init__(
        self,
        users: UserRepository,
        messages: MessageRepository,
        attachment_service: AttachmentService,
    ):
        self.processor = MessageProcessor(
            save_user=SaveUserStep(users),
            save_reply=SaveReplyStep(messages),
            save_message=SaveMessageStep(messages, users),
            attachment_service=attachment_service,
        )

    async def save_message(self, telegram_user, telegram_message):
        return await self.processor.process(
            telegram_user=telegram_user,
            telegram_message=telegram_message,
        )
