from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Import
from app.database.repositories.base import BaseRepository


class ImportRepository(BaseRepository[Import]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        import_id: int,
    ) -> Import | None:
        stmt = select(Import).where(
            Import.id == import_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_recent(
        self,
        limit: int = 100,
    ) -> list[Import]:
        stmt = (
            select(Import)
            .order_by(desc(Import.created_at))
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> Import:
        import_record = Import(**data)

        self.db.add(import_record)

        await self.db.commit()
        await self.db.refresh(import_record)

        return import_record

    async def save(
        self,
        import_record: Import,
    ) -> Import:
        self.db.add(import_record)

        await self.db.commit()
        await self.db.refresh(import_record)

        return import_record

    async def delete(
        self,
        import_record: Import,
    ) -> None:
        await self.db.delete(import_record)
        await self.db.commit()