from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Event
from app.database.repositories.base import BaseRepository


class EventRepository(BaseRepository[Event]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(self, event_id: int) -> Event | None:
        stmt = select(Event).where(Event.id == event_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Event | None:
        stmt = select(Event).where(Event.slug == slug)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Event]:
        stmt = (
            select(Event)
            .order_by(desc(Event.start_at))
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_published(self) -> list[Event]:
        stmt = (
            select(Event)
            .where(Event.is_published.is_(True))
            .order_by(desc(Event.start_at))
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> Event:
        event = Event(**data)

        self.db.add(event)

        await self.db.commit()
        await self.db.refresh(event)

        return event

    async def save(self, event: Event) -> Event:
        self.db.add(event)

        await self.db.commit()
        await self.db.refresh(event)

        return event

    async def delete(self, event: Event) -> None:
        await self.db.delete(event)
        await self.db.commit()