from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import UserOrganization
from app.database.repositories.base import BaseRepository


class UserOrganizationRepository(BaseRepository[UserOrganization]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(
        self,
        user_organization_id: int,
    ) -> UserOrganization | None:
        stmt = select(UserOrganization).where(
            UserOrganization.id == user_organization_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: int,
    ) -> list[UserOrganization]:
        stmt = (
            select(UserOrganization)
            .where(UserOrganization.user_id == user_id)
            .order_by(UserOrganization.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_by_organization(
        self,
        organization_id: int,
    ) -> list[UserOrganization]:
        stmt = (
            select(UserOrganization)
            .where(UserOrganization.organization_id == organization_id)
            .order_by(UserOrganization.id)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> UserOrganization:
        user_organization = UserOrganization(**data)

        self.db.add(user_organization)

        await self.db.commit()
        await self.db.refresh(user_organization)

        return user_organization

    async def save(
        self,
        user_organization: UserOrganization,
    ) -> UserOrganization:
        self.db.add(user_organization)

        await self.db.commit()
        await self.db.refresh(user_organization)

        return user_organization

    async def delete(
        self,
        user_organization: UserOrganization,
    ) -> None:
        await self.db.delete(user_organization)
        await self.db.commit()