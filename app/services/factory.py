from app.database.uow import UnitOfWork

from app.services.attachment_service import AttachmentService
# from app.services.member_sync_service import MemberSyncService
from app.services.message_processor.processor import MessageProcessor
from app.services.message_processor.steps.save_message import SaveMessageStep
from app.services.message_processor.steps.save_reply import SaveReplyStep
from app.services.message_processor.steps.save_user import SaveUserStep
from app.services.profile_service import ProfileService
from app.services.user_service import UserService


class ServiceFactory:
    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow

        self.attachments = AttachmentService(
            uow.attachments,
        )

        self.users = UserService(
            uow.users,
        )

        self.profiles = ProfileService(
            uow.profiles,
        )

       # self.member_sync = MemberSyncService(
        #    uow.users,
        #)

        self.message_processor = MessageProcessor(
            save_user=SaveUserStep(
                uow.users,
            ),
            save_reply=SaveReplyStep(
                uow.messages,
            ),
            save_message=SaveMessageStep(
                uow.messages,
            ),
            attachment_service=self.attachments,
        )