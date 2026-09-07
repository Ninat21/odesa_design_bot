from datetime import datetime

from sqlalchemy import case, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert_by_telegram_id(self, **data) -> User:
        stmt = insert(User).values(**data)
        fields_to_update = {
            field: getattr(stmt.excluded, field)
            for field in (
                "username",
                "first_name",
                "last_name",
                "is_bot",
                "language_code",
                "is_premium",
            )
        }
        stmt = stmt.on_conflict_do_update(
            index_elements=[User.telegram_id],
            set_=fields_to_update,
        ).returning(User)
        result = await self.db.execute(stmt.execution_options(populate_existing=True))
        return result.scalar_one()

    async def record_message_activity(
        self,
        user: User,
        message_date: datetime,
        is_reply: bool,
        has_media: bool,
    ) -> None:
        latest_message = case(
            (
                (User.last_message_at.is_(None))
                | (User.last_message_at < message_date),
                message_date,
            ),
            else_=User.last_message_at,
        )
        stmt = (
            update(User)
            .where(User.id == user.id)
            .values(
                messages_count=User.messages_count + 1,
                replies_count=User.replies_count + int(is_reply),
                media_count=User.media_count + int(has_media),
                last_message_at=latest_message,
                last_activity_at=latest_message,
            )
        )
        await self.db.execute(stmt)
        await self.db.refresh(user)

    async def mark_joined(self, user: User, joined_at: datetime) -> User:
        first_join = case(
            (User.joined_at.is_(None), joined_at),
            else_=User.joined_at,
        )
        first_seen = case(
            (User.first_seen_at.is_(None), joined_at),
            else_=User.first_seen_at,
        )
        await self.db.execute(
            update(User)
            .where(User.id == user.id)
            .values(
                is_member=True,
                joined_at=first_join,
                left_at=None,
                first_seen_at=first_seen,
                last_seen_at=joined_at,
            )
        )
        await self.db.refresh(user)
        return user

    async def mark_left(self, user: User, left_at: datetime) -> User:
        await self.db.execute(
            update(User)
            .where(User.id == user.id)
            .values(
                is_member=False,
                left_at=left_at,
                last_seen_at=left_at,
            )
        )
        await self.db.refresh(user)
        return user

    async def mark_present(self, user: User, observed_at: datetime) -> User:
        await self.db.execute(
            update(User)
            .where(User.id == user.id)
            .values(
                is_member=True,
                left_at=None,
                last_seen_at=observed_at,
            )
        )
        await self.db.refresh(user)
        return user

    async def create(self, **data) -> User:
        user = User(**data)

        self.db.add(user)

        await self.db.flush()
        await self.db.refresh(user)

        return user

    async def save(self, user: User) -> User:
        self.db.add(user)

        await self.db.flush()
        await self.db.refresh(user)

        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.flush()
