from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Tag
from app.database.repositories.base import BaseRepository


class TagRepository(BaseRepository[Tag]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        tag_id: int,
    ) -> Tag | None:
        stmt = select(Tag).where(
            Tag.id == tag_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        name: str,
    ) -> Tag | None:
        stmt = select(Tag).where(
            Tag.name == name
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Tag]:
        stmt = (
            select(Tag)
            .order_by(Tag.name)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> Tag:
        tag = Tag(**data)

        self.db.add(tag)

        await self.db.commit()
        await self.db.refresh(tag)

        return tag

    async def save(
        self,
        tag: Tag,
    ) -> Tag:
        self.db.add(tag)

        await self.db.commit()
        await self.db.refresh(tag)

        return tag

    async def delete(
        self,
        tag: Tag,
    ) -> None:
        await self.db.delete(tag)
        await self.db.commit()