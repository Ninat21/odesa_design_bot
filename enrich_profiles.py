import asyncio

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.database.database import SessionLocal
from app.database.models import Message, ProfileFact, User
from app.services.profile_extractor import extract_profile_facts


async def main() -> None:
    found = 0
    inserted = 0

    async with SessionLocal() as session:
        rows = await session.execute(
            select(Message, User.username)
            .join(User, Message.user_id == User.id)
            .where(Message.text.is_not(None), Message.text != "")
            .order_by(Message.id)
        )
        for message, username in rows:
            facts = extract_profile_facts(
                message.text,
                message.telegram_date,
                username,
            )
            for fact in facts:
                found += 1
                statement = (
                    insert(ProfileFact)
                    .values(
                        user_id=message.user_id,
                        fact_type=fact.fact_type,
                        value=fact.value,
                        source_type="chat_message",
                        source_key=f"message:{message.id}",
                        source_message_id=message.id,
                        confidence=fact.confidence,
                        verified=False,
                        inferred=False,
                        observed_at=message.telegram_date,
                    )
                    .on_conflict_do_nothing(constraint="uq_profile_fact_source")
                    .returning(ProfileFact.id)
                )
                if await session.scalar(statement) is not None:
                    inserted += 1
        await session.commit()

    print({"facts_found": found, "facts_inserted": inserted})


if __name__ == "__main__":
    asyncio.run(main())
