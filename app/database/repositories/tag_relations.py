from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import TagRelation
from app.database.repositories.base import BaseRepository


class TagRelationRepository(BaseRepository[TagRelation]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        relation_id: int,
    ) -> TagRelation | None:
        stmt = select(TagRelation).where(
            TagRelation.id == relation_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_tag(
        self,
        tag_id: int,
    ) -> list[TagRelation]:
        stmt = (
            select(TagRelation)
            .where(TagRelation.tag_id == tag_id)
            .order_by(TagRelation.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_by_entity(
        self,
        entity_type: str,
        entity_id: int,
    ) -> list[TagRelation]:
        stmt = (
            select(TagRelation)
            .where(
                TagRelation.entity_type == entity_type,
                TagRelation.entity_id == entity_id,
            )
            .order_by(TagRelation.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> TagRelation:
        relation = TagRelation(**data)

        self.db.add(relation)

        await self.db.commit()
        await self.db.refresh(relation)

        return relation

    async def save(
        self,
        relation: TagRelation,
    ) -> TagRelation:
        self.db.add(relation)

        await self.db.commit()
        await self.db.refresh(relation)

        return relation

    async def delete(
        self,
        relation: TagRelation,
    ) -> None:
        await self.db.delete(relation)
        await self.db.commit()