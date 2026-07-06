from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import EventFeedback
from app.database.repositories.base import BaseRepository


class EventFeedbackRepository(BaseRepository[EventFeedback]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(self, feedback_id: int) -> EventFeedback | None:
        stmt = select(EventFeedback).where(
            EventFeedback.id == feedback_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_event_and_user(
        self,
        event_id: int,
        user_id: int,
    ) -> EventFeedback | None:
        stmt = select(EventFeedback).where(
            EventFeedback.event_id == event_id,
            EventFeedback.user_id == user_id,
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_event(
        self,
        event_id: int,
    ) -> list[EventFeedback]:
        stmt = (
            select(EventFeedback)
            .where(EventFeedback.event_id == event_id)
            .order_by(EventFeedback.created_at.desc())
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> EventFeedback:
        feedback = EventFeedback(**data)

        self.db.add(feedback)

        await self.db.commit()
        await self.db.refresh(feedback)

        return feedback

    async def save(self, feedback: EventFeedback) -> EventFeedback:
        self.db.add(feedback)

        await self.db.commit()
        await self.db.refresh(feedback)

        return feedback

    async def delete(self, feedback: EventFeedback) -> None:
        await self.db.delete(feedback)
        await self.db.commit()