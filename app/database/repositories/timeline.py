from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Timeline
from app.database.repositories.base import BaseRepository


class TimelineRepository(BaseRepository[Timeline]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        timeline_id: int,
    ) -> Timeline | None:
        stmt = select(Timeline).where(
            Timeline.id == timeline_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: int,
    ) -> list[Timeline]:
        stmt = (
            select(Timeline)
            .where(Timeline.user_id == user_id)
            .order_by(desc(Timeline.created_at))
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_recent(
        self,
        limit: int = 100,
    ) -> list[Timeline]:
        stmt = (
            select(Timeline)
            .order_by(desc(Timeline.created_at))
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> Timeline:
        timeline = Timeline(**data)

        self.db.add(timeline)

        await self.db.commit()
        await self.db.refresh(timeline)

        return timeline

    async def save(
        self,
        timeline: Timeline,
    ) -> Timeline:
        self.db.add(timeline)

        await self.db.commit()
        await self.db.refresh(timeline)

        return timeline

    async def delete(
        self,
        timeline: Timeline,
    ) -> None:
        await self.db.delete(timeline)
        await self.db.commit()