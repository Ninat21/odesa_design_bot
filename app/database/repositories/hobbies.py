from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Hobby
from app.database.repositories.base import BaseRepository


class HobbyRepository(BaseRepository[Hobby]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        hobby_id: int,
    ) -> Hobby | None:
        stmt = select(Hobby).where(
            Hobby.id == hobby_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        name: str,
    ) -> Hobby | None:
        stmt = select(Hobby).where(
            Hobby.name == name
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Hobby]:
        stmt = (
            select(Hobby)
            .order_by(Hobby.name)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> Hobby:
        hobby = Hobby(**data)

        self.db.add(hobby)

        await self.db.commit()
        await self.db.refresh(hobby)

        return hobby

    async def save(
        self,
        hobby: Hobby,
    ) -> Hobby:
        self.db.add(hobby)

        await self.db.commit()
        await self.db.refresh(hobby)

        return hobby

    async def delete(
        self,
        hobby: Hobby,
    ) -> None:
        await self.db.delete(hobby)
        await self.db.commit()