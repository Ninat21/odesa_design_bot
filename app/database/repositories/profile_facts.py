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

    async def get_by_id(self, fact_id: int) -> ProfileFact | None:
        stmt = select(ProfileFact).where(ProfileFact.id == fact_id)
        return (await self.db.execute(stmt)).scalar_one_or_none()

    async def verify(self, fact: ProfileFact) -> ProfileFact:
        fact.verified = True
        fact.inferred = False
        fact.confidence = 1
        self.db.add(fact)
        await self.db.flush()
        await self.db.refresh(fact)
        return fact

    async def update_value(self, fact: ProfileFact, value: str) -> ProfileFact:
        fact.value = value
        fact.source_type = "admin_edit"
        fact.source_key = f"admin:{fact.id}"
        fact.source_message_id = None
        fact.verified = True
        fact.inferred = False
        fact.confidence = 1
        self.db.add(fact)
        await self.db.flush()
        await self.db.refresh(fact)
        return fact

    async def delete(self, fact: ProfileFact) -> None:
        await self.db.delete(fact)
        await self.db.flush()
