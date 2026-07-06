from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import UserInterest
from app.database.repositories.base import BaseRepository


class UserInterestRepository(BaseRepository[UserInterest]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        user_interest_id: int,
    ) -> UserInterest | None:
        stmt = select(UserInterest).where(
            UserInterest.id == user_interest_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: int,
    ) -> list[UserInterest]:
        stmt = (
            select(UserInterest)
            .where(UserInterest.user_id == user_id)
            .order_by(UserInterest.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_by_interest(
        self,
        interest_id: int,
    ) -> list[UserInterest]:
        stmt = (
            select(UserInterest)
            .where(UserInterest.interest_id == interest_id)
            .order_by(UserInterest.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> UserInterest:
        user_interest = UserInterest(**data)

        self.db.add(user_interest)

        await self.db.commit()
        await self.db.refresh(user_interest)

        return user_interest

    async def save(
        self,
        user_interest: UserInterest,
    ) -> UserInterest:
        self.db.add(user_interest)

        await self.db.commit()
        await self.db.refresh(user_interest)

        return user_interest

    async def delete(
        self,
        user_interest: UserInterest,
    ) -> None:
        await self.db.delete(user_interest)
        await self.db.commit()