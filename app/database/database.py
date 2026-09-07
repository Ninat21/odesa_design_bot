import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не знайдено в .env")


def normalize_database_url(database_url: str) -> str:
    """Use the async PostgreSQL driver for provider-supplied connection URLs."""
    if database_url.startswith("postgres://"):
        database_url = "postgresql+asyncpg://" + database_url.removeprefix(
            "postgres://"
        )
    elif database_url.startswith("postgresql://"):
        database_url = "postgresql+asyncpg://" + database_url.removeprefix(
            "postgresql://"
        )

    return database_url.replace("sslmode=require", "ssl=require")

engine = create_async_engine(
    normalize_database_url(DATABASE_URL),
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass
