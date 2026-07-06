from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Interest
from app.database.repositories.base import BaseRepository


class InterestRepository(BaseRepository[Interest]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        interest_id: int,
    ) -> Interest | None:
        stmt = select(Interest).where(
            Interest.id == interest_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        name: str,
    ) -> Interest | None:
        stmt = select(Interest).where(
            Interest.name == name
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Interest]:
        stmt = (
            select(Interest)
            .order_by(Interest.name)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> Interest:
        interest = Interest(**data)

        self.db.add(interest)

        await self.db.commit()
        await self.db.refresh(interest)

        return interest

    async def save(
        self,
        interest: Interest,
    ) -> Interest:
        self.db.add(interest)

        await self.db.commit()
        await self.db.refresh(interest)

        return interest

    async def delete(
        self,
        interest: Interest,
    ) -> None:
        await self.db.delete(interest)
        await self.db.commit()