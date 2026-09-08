import asyncio
import re
from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from telethon.tl.functions.users import GetFullUserRequest

from app.config import Config
from app.database.database import SessionLocal
from app.database.models import ProfileFact, User
from app.telethon.client import client

URL_RE = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)


def fact_type_for_url(url: str) -> str:
    lowered = url.lower()
    if any(domain in lowered for domain in ("instagram.com", "linkedin.com")):
        return "social"
    if "behance.net" in lowered:
        return "portfolio"
    return "website"


async def main() -> None:
    await client.start()
    found_bios = 0
    saved_facts = 0

    try:
        entity = await client.get_entity(Config.GROUP_ID)
        async with SessionLocal() as session:
            users = dict(
                (
                    await session.execute(select(User.telegram_id, User.id))
                ).all()
            )
            async for member in client.iter_participants(entity):
                user_id = users.get(member.id)
                if user_id is None:
                    continue
                full = await client(GetFullUserRequest(member))
                about = (getattr(full.full_user, "about", None) or "").strip()
                if not about:
                    continue

                found_bios += 1
                await session.execute(
                    delete(ProfileFact).where(
                        ProfileFact.user_id == user_id,
                        ProfileFact.source_type == "telegram_profile",
                    )
                )
                values = [
                    {
                        "user_id": user_id,
                        "fact_type": "bio",
                        "value": about,
                        "source_type": "telegram_profile",
                        "source_key": "telegram_bio",
                        "confidence": 1.0,
                        "verified": True,
                        "inferred": False,
                        "observed_at": datetime.now(UTC),
                    }
                ]
                for index, url in enumerate(URL_RE.findall(about)):
                    clean_url = url.rstrip(".,;:!?)]}")
                    values.append(
                        {
                            "user_id": user_id,
                            "fact_type": fact_type_for_url(clean_url),
                            "value": clean_url,
                            "source_type": "telegram_profile",
                            "source_key": f"telegram_bio_url:{index}",
                            "confidence": 1.0,
                            "verified": True,
                            "inferred": False,
                            "observed_at": datetime.now(UTC),
                        }
                    )
                await session.execute(insert(ProfileFact).values(values))
                saved_facts += len(values)

            await session.commit()
    finally:
        await client.disconnect()

    print({"profiles_with_bio": found_bios, "facts_saved": saved_facts})


if __name__ == "__main__":
    asyncio.run(main())
