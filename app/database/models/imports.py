from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base
from app.database.models.base import TimestampMixin


class Import(Base, TimestampMixin):
    __tablename__ = "imports"

    __table_args__ = (
        Index("ix_imports_source", "source"),
        Index("ix_imports_status", "status"),
        Index("ix_imports_started_at", "started_at"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    file_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    imported_users: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    imported_messages: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    skipped_records: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )