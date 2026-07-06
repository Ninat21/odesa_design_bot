from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Profile
from app.database.repositories.base import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_user_id(self, user_id: int) -> Profile | None:
        stmt = select(Profile).where(Profile.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **data) -> Profile:
        profile = Profile(**data)

        self.db.add(profile)

        await self.db.commit()
        await self.db.refresh(profile)

        return profile

    async def save(self, profile: Profile) -> Profile:
        self.db.add(profile)

        await self.db.commit()
        await self.db.refresh(profile)

        return profile

    async def delete(self, profile: Profile) -> None:
        await self.db.delete(profile)
        await self.db.commit()