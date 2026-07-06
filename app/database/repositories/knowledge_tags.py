from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import KnowledgeTag
from app.database.repositories.base import BaseRepository


class KnowledgeTagRepository(BaseRepository[KnowledgeTag]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        tag_id: int,
    ) -> KnowledgeTag | None:
        stmt = select(KnowledgeTag).where(
            KnowledgeTag.id == tag_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_article(
        self,
        article_id: int,
    ) -> list[KnowledgeTag]:
        stmt = (
            select(KnowledgeTag)
            .where(KnowledgeTag.knowledge_article_id == article_id)
            .order_by(KnowledgeTag.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> KnowledgeTag:
        tag = KnowledgeTag(**data)

        self.db.add(tag)

        await self.db.commit()
        await self.db.refresh(tag)

        return tag

    async def save(
        self,
        tag: KnowledgeTag,
    ) -> KnowledgeTag:
        self.db.add(tag)

        await self.db.commit()
        await self.db.refresh(tag)

        return tag

    async def delete(
        self,
        tag: KnowledgeTag,
    ) -> None:
        await self.db.delete(tag)
        await self.db.commit()