from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import KnowledgeSource
from app.database.repositories.base import BaseRepository


class KnowledgeSourceRepository(BaseRepository[KnowledgeSource]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        source_id: int,
    ) -> KnowledgeSource | None:
        stmt = select(KnowledgeSource).where(
            KnowledgeSource.id == source_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_article(
        self,
        article_id: int,
    ) -> list[KnowledgeSource]:
        stmt = (
            select(KnowledgeSource)
            .where(KnowledgeSource.knowledge_article_id == article_id)
            .order_by(KnowledgeSource.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> KnowledgeSource:
        source = KnowledgeSource(**data)

        self.db.add(source)

        await self.db.commit()
        await self.db.refresh(source)

        return source

    async def save(
        self,
        source: KnowledgeSource,
    ) -> KnowledgeSource:
        self.db.add(source)

        await self.db.commit()
        await self.db.refresh(source)

        return source

    async def delete(
        self,
        source: KnowledgeSource,
    ) -> None:
        await self.db.delete(source)
        await self.db.commit()