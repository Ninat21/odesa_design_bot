from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Organization
from app.database.repositories.base import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(self, organization_id: int) -> Organization | None:
        stmt = select(Organization).where(
            Organization.id == organization_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Organization | None:
        stmt = select(Organization).where(
            Organization.slug == slug
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Organization]:
        stmt = select(Organization).order_by(Organization.name)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> Organization:
        organization = Organization(**data)

        self.db.add(organization)

        await self.db.commit()
        await self.db.refresh(organization)

        return organization

    async def save(self, organization: Organization) -> Organization:
        self.db.add(organization)

        await self.db.commit()
        await self.db.refresh(organization)

        return organization

    async def delete(self, organization: Organization) -> None:
        await self.db.delete(organization)
        await self.db.commit()