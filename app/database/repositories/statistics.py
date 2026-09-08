from datetime import UTC, datetime, timedelta

from sqlalchemy import and_, func, or_, select

from app.database.models import Message, User
from app.database.repositories.base import BaseRepository


class StatisticsRepository(BaseRepository):
    async def get_current_members(self) -> list[User]:
        stmt = (
            select(User)
            .where(
                User.is_member.is_(True),
            )
            .order_by(
                func.lower(func.coalesce(User.first_name, User.username, "")),
                func.lower(func.coalesce(User.last_name, "")),
                User.telegram_id,
            )
        )

        result = await self.db.execute(stmt)
        return list(result.scalars())

    async def get_left_members(self) -> list[User]:
        stmt = (
            select(User)
            .where(
                User.is_member.is_(False),
                User.is_bot.is_(False),
            )
            .order_by(
                User.left_at.desc().nullslast(),
                func.lower(func.coalesce(User.first_name, User.username, "")),
                User.telegram_id,
            )
        )

        result = await self.db.execute(stmt)
        return list(result.scalars())

    async def get_totals(self) -> tuple[int, int, int]:
        current_users = await self.db.scalar(
            select(func.count(User.id)).where(
                User.is_member.is_(True),
                User.is_bot.is_(False),
            )
        )
        left_users = await self.db.scalar(
            select(func.count(User.id)).where(
                User.is_member.is_(False),
                User.is_bot.is_(False),
            )
        )
        messages = await self.db.scalar(select(func.count(Message.id)))
        return current_users or 0, left_users or 0, messages or 0

    async def get_top_users(
        self,
        limit: int,
        days: int | None = None,
    ):

        stmt = select(
            User,
            func.count(Message.id).label("messages"),
        ).join(
            Message,
            Message.user_id == User.id,
        ).where(
            User.is_member.is_(True),
            User.is_bot.is_(False),
        )

        if days is not None:
            date_from = datetime.now(UTC) - timedelta(days=days)

            stmt = stmt.where(
                Message.telegram_date >= date_from,
            )

        stmt = (
            stmt.group_by(User.id)
            .order_by(
                func.count(Message.id).desc(),
                User.first_name,
            )
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return result.all()

    async def get_users_without_messages(self):
        stmt = (
            select(User)
            .outerjoin(
                Message,
                Message.user_id == User.id,
            )
            .where(
                User.is_member.is_(True),
                User.is_bot.is_(False),
            )
            .group_by(User.id)
            .having(func.count(Message.id) == 0)
            .order_by(User.first_name)
        )

        result = await self.db.execute(stmt)

        return list(result.scalars())

    async def get_users_with_one_message(self):

        stmt = (
            select(
                User,
                func.count(Message.id).label("messages"),
            )
            .join(
                Message,
                Message.user_id == User.id,
            )
            .where(
                User.is_member.is_(True),
                User.is_bot.is_(False),
            )
            .group_by(User.id)
            .having(func.count(Message.id) == 1)
            .order_by(User.first_name)
        )

        result = await self.db.execute(stmt)

        return result.all()

    async def get_inactive_users(
        self,
        days: int,
    ):

        border = datetime.now(UTC) - timedelta(days=days)
        subquery = (
            select(
                Message.user_id,
                func.max(Message.telegram_date).label("last_message"),
                func.count(Message.id).label(
                    "messages",
                ),
            )
            .group_by(Message.user_id)
            .subquery()
        )

        stmt = (
            select(
                User,
                subquery.c.messages,
                subquery.c.last_message,
            )
            .join(
                subquery,
                User.id == subquery.c.user_id,
            )
            .where(
                and_(
                    subquery.c.messages > 0,
                    subquery.c.last_message < border,
                    (User.joined_at.is_(None)) | (User.joined_at < border),
                    User.is_member.is_(True),
                    User.is_bot.is_(False),
                )
            )
            .order_by(
                subquery.c.last_message,
            )
        )

        result = await self.db.execute(stmt)

        return result.all()

    async def get_inactive_members(self, days: int):
        border = datetime.now(UTC) - timedelta(days=days)
        activity = (
            select(
                Message.user_id,
                func.max(Message.telegram_date).label("last_message"),
                func.count(Message.id).label("messages"),
            )
            .group_by(Message.user_id)
            .subquery()
        )

        stmt = (
            select(
                User,
                func.coalesce(activity.c.messages, 0).label("messages"),
                activity.c.last_message,
            )
            .outerjoin(activity, User.id == activity.c.user_id)
            .where(
                User.is_member.is_(True),
                User.is_bot.is_(False),
                User.joined_at <= border,
                or_(
                    activity.c.last_message.is_(None),
                    activity.c.last_message < border,
                ),
            )
            .order_by(
                activity.c.last_message.asc().nullsfirst(),
                func.lower(func.coalesce(User.first_name, User.username, "")),
                User.telegram_id,
            )
        )

        result = await self.db.execute(stmt)
        return result.all()

    async def get_oldest_members(
        self,
        limit: int,
    ):

        stmt = (
            select(User)
            .where(
                User.is_member.is_(True),
                User.is_bot.is_(False),
                User.joined_at.is_not(None),
            )
            .order_by(User.joined_at)
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return list(result.scalars())

    async def get_new_members(
        self,
        days: int,
    ):

        border = datetime.now(UTC) - timedelta(days=days)

        stmt = (
            select(User)
            .where(
                User.joined_at >= border,
                User.is_member.is_(True),
                User.is_bot.is_(False),
            )
            .order_by(
                User.joined_at.desc(),
            )
        )

        result = await self.db.execute(stmt)

        return list(result.scalars())
