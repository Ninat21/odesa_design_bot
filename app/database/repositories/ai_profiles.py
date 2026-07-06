from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import AIProfile
from app.database.repositories.base import BaseRepository


class AIProfileRepository(BaseRepository[AIProfile]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        profile_id: int,
    ) -> AIProfile | None:
        stmt = select(AIProfile).where(
            AIProfile.id == profile_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> AIProfile | None:
        stmt = select(AIProfile).where(
            AIProfile.user_id == user_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **data) -> AIProfile:
        profile = AIProfile(**data)

        self.db.add(profile)

        await self.db.commit()
        await self.db.refresh(profile)

        return profile

    async def save(
        self,
        profile: AIProfile,
    ) -> AIProfile:
        self.db.add(profile)

        await self.db.commit()
        await self.db.refresh(profile)

        return profile

    async def delete(
        self,
        profile: AIProfile,
    ) -> None:
        await self.db.delete(profile)
        await self.db.commit()