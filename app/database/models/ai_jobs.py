from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base
from app.database.models.base import TimestampMixin


class AIJob(Base, TimestampMixin):
    __tablename__ = "ai_jobs"

    __table_args__ = (
        Index("ix_ai_jobs_status", "status"),
        Index("ix_ai_jobs_job_type", "job_type"),
        Index("ix_ai_jobs_entity_type", "entity_type"),
        Index("ix_ai_jobs_entity_id", "entity_id"),
        Index("ix_ai_jobs_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    job_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    entity_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    priority: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    ai_model: Mapped[str | None] = mapped_column(
        String(100),
    )

    attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )