from datetime import datetime

from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Message
from app.database.repositories.base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        message_id: int,
    ) -> Message | None:
        stmt = select(Message).where(
            Message.id == message_id,
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_telegram_message_id(
        self,
        chat_id: int,
        telegram_message_id: int,
    ) -> Message | None:

        stmt = select(Message).where(
            and_(
                Message.chat_id == chat_id,
                Message.telegram_message_id == telegram_message_id,
            )
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Message]:

        stmt = (
            select(Message)
            .where(Message.user_id == user_id)
            .order_by(desc(Message.telegram_date))
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def list_by_chat(
        self,
        chat_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Message]:

        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(desc(Message.telegram_date))
            .limit(limit)
            .offset(offset)
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def list_between_dates(
        self,
        date_from: datetime,
        date_to: datetime,
    ) -> list[Message]:

        stmt = (
            select(Message)
            .where(
                Message.telegram_date.between(
                    date_from,
                    date_to,
                )
            )
            .order_by(Message.telegram_date)
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def create(
        self,
        **data,
    ) -> Message:

        message = Message(**data)

        self.db.add(message)

        await self.db.flush()
        await self.db.refresh(message)

        return message

    async def save(
        self,
        message: Message,
    ) -> Message:

        self.db.add(message)

        await self.db.flush()
        await self.db.refresh(message)

        return message

    async def delete(
        self,
        message: Message,
    ) -> None:

        await self.db.delete(message)

        await self.db.flush()