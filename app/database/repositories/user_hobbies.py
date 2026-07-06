from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import UserHobby
from app.database.repositories.base import BaseRepository


class UserHobbyRepository(BaseRepository[UserHobby]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        user_hobby_id: int,
    ) -> UserHobby | None:
        stmt = select(UserHobby).where(
            UserHobby.id == user_hobby_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: int,
    ) -> list[UserHobby]:
        stmt = (
            select(UserHobby)
            .where(UserHobby.user_id == user_id)
            .order_by(UserHobby.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_by_hobby(
        self,
        hobby_id: int,
    ) -> list[UserHobby]:
        stmt = (
            select(UserHobby)
            .where(UserHobby.hobby_id == hobby_id)
            .order_by(UserHobby.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> UserHobby:
        user_hobby = UserHobby(**data)

        self.db.add(user_hobby)

        await self.db.commit()
        await self.db.refresh(user_hobby)

        return user_hobby

    async def save(
        self,
        user_hobby: UserHobby,
    ) -> UserHobby:
        self.db.add(user_hobby)

        await self.db.commit()
        await self.db.refresh(user_hobby)

        return user_hobby

    async def delete(
        self,
        user_hobby: UserHobby,
    ) -> None:
        await self.db.delete(user_hobby)
        await self.db.commit()