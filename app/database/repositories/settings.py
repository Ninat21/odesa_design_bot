from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Setting
from app.database.repositories.base import BaseRepository


class SettingRepository(BaseRepository[Setting]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        setting_id: int,
    ) -> Setting | None:
        stmt = select(Setting).where(
            Setting.id == setting_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_key(
        self,
        key: str,
    ) -> Setting | None:
        stmt = select(Setting).where(
            Setting.key == key
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Setting]:
        stmt = (
            select(Setting)
            .order_by(Setting.key)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> Setting:
        setting = Setting(**data)

        self.db.add(setting)

        await self.db.commit()
        await self.db.refresh(setting)

        return setting

    async def save(
        self,
        setting: Setting,
    ) -> Setting:
        self.db.add(setting)

        await self.db.commit()
        await self.db.refresh(setting)

        return setting

    async def delete(
        self,
        setting: Setting,
    ) -> None:
        await self.db.delete(setting)
        await self.db.commit()