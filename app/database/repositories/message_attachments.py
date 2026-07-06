from sqlalchemy import select
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
        stmt = select(MessageAttachment).where(
            MessageAttachment.id == attachment_id
        )

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

    async def create(self, **data) -> MessageAttachment:
        attachment = MessageAttachment(**data)

        self.db.add(attachment)

        await self.db.commit()
        await self.db.refresh(attachment)

        return attachment

    async def save(
        self,
        attachment: MessageAttachment,
    ) -> MessageAttachment:
        self.db.add(attachment)

        await self.db.commit()
        await self.db.refresh(attachment)

        return attachment

    async def delete(
        self,
        attachment: MessageAttachment,
    ) -> None:
        await self.db.delete(attachment)
        await self.db.commit()