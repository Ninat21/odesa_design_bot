from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, Text

from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    username: Mapped[str | None] = mapped_column(String(255))

    first_name: Mapped[str | None] = mapped_column(String(255))

    last_name: Mapped[str | None] = mapped_column(String(255))

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    message_id: Mapped[int] = mapped_column(Integer)

    telegram_id: Mapped[int] = mapped_column(BigInteger)

    chat_id: Mapped[int] = mapped_column(BigInteger)

    date: Mapped[datetime] = mapped_column(DateTime)

    text: Mapped[str | None] = mapped_column(Text)