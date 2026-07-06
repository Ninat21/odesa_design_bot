from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import SavedMessage
from app.database.repositories.base import BaseRepository


class SavedMessageRepository(BaseRepository[SavedMessage]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(self, saved_message_id: int) -> SavedMessage | None:
        stmt = select(SavedMessage).where(
            SavedMessage.id == saved_message_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_message_id(
        self,
        message_id: int,
    ) -> SavedMessage | None:
        stmt = select(SavedMessage).where(
            SavedMessage.message_id == message_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[SavedMessage]:
        stmt = (
            select(SavedMessage)
            .order_by(SavedMessage.created_at.desc())
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> SavedMessage:
        saved_message = SavedMessage(**data)

        self.db.add(saved_message)

        await self.db.commit()
        await self.db.refresh(saved_message)

        return saved_message

    async def save(self, saved_message: SavedMessage) -> SavedMessage:
        self.db.add(saved_message)

        await self.db.commit()
        await self.db.refresh(saved_message)

        return saved_message

    async def delete(self, saved_message: SavedMessage) -> None:
        await self.db.delete(saved_message)
        await self.db.commit()