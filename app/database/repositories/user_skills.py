from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import UserSkill
from app.database.repositories.base import BaseRepository


class UserSkillRepository(BaseRepository[UserSkill]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        user_skill_id: int,
    ) -> UserSkill | None:
        stmt = select(UserSkill).where(
            UserSkill.id == user_skill_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: int,
    ) -> list[UserSkill]:
        stmt = (
            select(UserSkill)
            .where(UserSkill.user_id == user_id)
            .order_by(UserSkill.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_by_skill(
        self,
        skill_id: int,
    ) -> list[UserSkill]:
        stmt = (
            select(UserSkill)
            .where(UserSkill.skill_id == skill_id)
            .order_by(UserSkill.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> UserSkill:
        user_skill = UserSkill(**data)

        self.db.add(user_skill)

        await self.db.commit()
        await self.db.refresh(user_skill)

        return user_skill

    async def save(
        self,
        user_skill: UserSkill,
    ) -> UserSkill:
        self.db.add(user_skill)

        await self.db.commit()
        await self.db.refresh(user_skill)

        return user_skill

    async def delete(
        self,
        user_skill: UserSkill,
    ) -> None:
        await self.db.delete(user_skill)
        await self.db.commit()