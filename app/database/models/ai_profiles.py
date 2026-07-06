from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class AIProfile(Base, TimestampMixin):
    __tablename__ = "ai_profiles"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            name="uq_ai_profiles_user_id",
        ),
        Index("ix_ai_profiles_user_id", "user_id"),
        Index("ix_ai_profiles_last_analyzed_at", "last_analyzed_at"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
    )

    personality: Mapped[str | None] = mapped_column(
        Text,
    )

    strengths: Mapped[str | None] = mapped_column(
        Text,
    )

    growth_areas: Mapped[str | None] = mapped_column(
        Text,
    )

    communication_style: Mapped[str | None] = mapped_column(
        Text,
    )

    activity_summary: Mapped[str | None] = mapped_column(
        Text,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    confidence: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
    )

    last_analyzed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    user = relationship(
        "User",
        back_populates="ai_profile",
    )