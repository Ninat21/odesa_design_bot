from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import KnowledgeArticle
from app.database.repositories.base import BaseRepository


class KnowledgeArticleRepository(BaseRepository[KnowledgeArticle]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        article_id: int,
    ) -> KnowledgeArticle | None:
        stmt = select(KnowledgeArticle).where(
            KnowledgeArticle.id == article_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[KnowledgeArticle]:
        stmt = (
            select(KnowledgeArticle)
            .order_by(desc(KnowledgeArticle.created_at))
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_published(self) -> list[KnowledgeArticle]:
        stmt = (
            select(KnowledgeArticle)
            .where(KnowledgeArticle.is_published.is_(True))
            .order_by(desc(KnowledgeArticle.created_at))
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> KnowledgeArticle:
        article = KnowledgeArticle(**data)

        self.db.add(article)

        await self.db.commit()
        await self.db.refresh(article)

        return article

    async def save(
        self,
        article: KnowledgeArticle,
    ) -> KnowledgeArticle:
        self.db.add(article)

        await self.db.commit()
        await self.db.refresh(article)

        return article

    async def delete(
        self,
        article: KnowledgeArticle,
    ) -> None:
        await self.db.delete(article)
        await self.db.commit()