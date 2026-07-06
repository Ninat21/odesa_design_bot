from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Skill
from app.database.repositories.base import BaseRepository


class SkillRepository(BaseRepository[Skill]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        skill_id: int,
    ) -> Skill | None:
        stmt = select(Skill).where(
            Skill.id == skill_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        name: str,
    ) -> Skill | None:
        stmt = select(Skill).where(
            Skill.name == name
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Skill]:
        stmt = (
            select(Skill)
            .order_by(Skill.name)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> Skill:
        skill = Skill(**data)

        self.db.add(skill)

        await self.db.commit()
        await self.db.refresh(skill)

        return skill

    async def save(
        self,
        skill: Skill,
    ) -> Skill:
        self.db.add(skill)

        await self.db.commit()
        await self.db.refresh(skill)

        return skill

    async def delete(
        self,
        skill: Skill,
    ) -> None:
        await self.db.delete(skill)
        await self.db.commit()