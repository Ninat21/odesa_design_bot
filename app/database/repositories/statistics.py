from datetime import UTC, datetime, timedelta

from sqlalchemy import and_, func, select

from app.database.models import Message, User
from app.database.repositories.base import BaseRepository


class StatisticsRepository(BaseRepository):

    async def get_top_users(
        self,
        limit: int,
        days: int | None = None,
    ):

        stmt = (
            select(
                User,
                func.count(Message.id).label("messages"),
            )
            .join(
                Message,
                Message.user_id == User.id,
            )
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
                func.max(Message.telegram_date).label(
                    "last_message"
                ),
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
                    User.created_at < border,
                )
            )
            .order_by(
                subquery.c.last_message,
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
            .order_by(User.created_at)
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
                User.created_at >= border,
            )
            .order_by(
                User.created_at.desc(),
            )
        )

        result = await self.db.execute(stmt)

        return list(result.scalars())