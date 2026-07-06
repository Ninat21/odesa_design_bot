from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **data) -> User:
        user = User(**data)

        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def save(self, user: User) -> User:
        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()

   