from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Message, ProfileFact
from app.database.repositories.base import BaseRepository


class ProfileFactRepository(BaseRepository[ProfileFact]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def list_with_sources(self, user_id: int):
        stmt = (
            select(ProfileFact, Message)
            .outerjoin(Message, ProfileFact.source_message_id == Message.id)
            .where(ProfileFact.user_id == user_id)
            .order_by(
                ProfileFact.verified.desc(),
                ProfileFact.confidence.desc().nullslast(),
                ProfileFact.fact_type,
            )
        )
        return (await self.db.execute(stmt)).all()
