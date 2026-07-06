from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Notification
from app.database.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(self, notification_id: int) -> Notification | None:
        stmt = select(Notification).where(
            Notification.id == notification_id
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: int,
    ) -> list[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_unread(
        self,
        user_id: int,
    ) -> list[Notification]:
        stmt = (
            select(Notification)
            .where(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
            .order_by(Notification.created_at.desc())
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **data) -> Notification:
        notification = Notification(**data)

        self.db.add(notification)

        await self.db.commit()
        await self.db.refresh(notification)

        return notification

    async def save(self, notification: Notification) -> Notification:
        self.db.add(notification)

        await self.db.commit()
        await self.db.refresh(notification)

        return notification

    async def delete(self, notification: Notification) -> None:
        await self.db.delete(notification)
        await self.db.commit()