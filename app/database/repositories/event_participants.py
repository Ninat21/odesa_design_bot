from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import EventParticipant
from app.database.repositories.base import BaseRepository


class EventParticipantRepository(BaseRepository[EventParticipant]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(self, participant_id: int) -> EventParticipant | None:
        stmt = select(EventParticipant).where(
            EventParticipant.id == participant_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_event_and_user(
        self,
        event_id: int,
        user_id: int,
    ) -> EventParticipant | None:
        stmt = select(EventParticipant).where(
            EventParticipant.event_id == event_id,
            EventParticipant.user_id == user_id,
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_event(
        self,
        event_id: int,
    ) -> list[EventParticipant]:
        stmt = (
            select(EventParticipant)
            .where(EventParticipant.event_id == event_id)
            .order_by(EventParticipant.registered_at)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_by_user(
        self,
        user_id: int,
    ) -> list[EventParticipant]:
        stmt = (
            select(EventParticipant)
            .where(EventParticipant.user_id == user_id)
            .order_by(EventParticipant.registered_at.desc())
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> EventParticipant:
        participant = EventParticipant(**data)

        self.db.add(participant)

        await self.db.commit()
        await self.db.refresh(participant)

        return participant

    async def save(self, participant: EventParticipant) -> EventParticipant:
        self.db.add(participant)

        await self.db.commit()
        await self.db.refresh(participant)

        return participant

    async def delete(self, participant: EventParticipant) -> None:
        await self.db.delete(participant)
        await self.db.commit()