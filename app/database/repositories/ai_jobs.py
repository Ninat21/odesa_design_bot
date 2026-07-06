from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import AIJob
from app.database.repositories.base import BaseRepository


class AIJobRepository(BaseRepository[AIJob]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        job_id: int,
    ) -> AIJob | None:
        stmt = select(AIJob).where(
            AIJob.id == job_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_pending(
        self,
    ) -> list[AIJob]:
        stmt = (
            select(AIJob)
            .where(AIJob.status == "pending")
            .order_by(AIJob.created_at)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_recent(
        self,
        limit: int = 100,
    ) -> list[AIJob]:
        stmt = (
            select(AIJob)
            .order_by(desc(AIJob.created_at))
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> AIJob:
        job = AIJob(**data)

        self.db.add(job)

        await self.db.commit()
        await self.db.refresh(job)

        return job

    async def save(
        self,
        job: AIJob,
    ) -> AIJob:
        self.db.add(job)

        await self.db.commit()
        await self.db.refresh(job)

        return job

    async def delete(
        self,
        job: AIJob,
    ) -> None:
        await self.db.delete(job)
        await self.db.commit()