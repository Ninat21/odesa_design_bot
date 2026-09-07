from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import MessageAttachment
from app.database.repositories.base import BaseRepository


class MessageAttachmentRepository(BaseRepository[MessageAttachment]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        attachment_id: int,
    ) -> MessageAttachment | None:
        stmt = select(MessageAttachment).where(MessageAttachment.id == attachment_id)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_message(
        self,
        message_id: int,
    ) -> list[MessageAttachment]:
        stmt = (
            select(MessageAttachment)
            .where(MessageAttachment.message_id == message_id)
            .order_by(MessageAttachment.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_message_and_unique_file_id(
        self,
        message_id: int,
        unique_file_id: str,
    ) -> MessageAttachment | None:
        stmt = select(MessageAttachment).where(
            MessageAttachment.message_id == message_id,
            MessageAttachment.telegram_unique_file_id == unique_file_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **data) -> MessageAttachment:
        attachment = MessageAttachment(**data)

        self.db.add(attachment)

        await self.db.flush()
        await self.db.refresh(attachment)

        return attachment

    async def create_if_missing(self, **data) -> MessageAttachment:
        stmt = (
            insert(MessageAttachment)
            .values(**data)
            .on_conflict_do_nothing(
                constraint="uq_message_attachments_message_file",
            )
            .returning(MessageAttachment)
        )
        result = await self.db.execute(stmt)
        attachment = result.scalar_one_or_none()

        if attachment is not None:
            return attachment

        existing = await self.get_by_message_and_unique_file_id(
            message_id=data["message_id"],
            unique_file_id=data["telegram_unique_file_id"],
        )
        if existing is None:
            raise RuntimeError("Attachment insert was ignored but no row was found")

        return existing

    async def save(
        self,
        attachment: MessageAttachment,
    ) -> MessageAttachment:
        self.db.add(attachment)

        await self.db.flush()
        await self.db.refresh(attachment)

        return attachment

    async def delete(
        self,
        attachment: MessageAttachment,
    ) -> None:
        await self.db.delete(attachment)
        await self.db.flush()
