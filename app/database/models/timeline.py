from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Index,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class Timeline(Base, TimestampMixin):
    __tablename__ = "timeline"

    __table_args__ = (
        Index("ix_timeline_user_id", "user_id"),
        Index("ix_timeline_event_type", "event_type"),
        Index("ix_timeline_entity_type", "entity_type"),
        Index("ix_timeline_entity_id", "entity_id"),
        Index("ix_timeline_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    entity_id: Mapped[int | None] = mapped_column(
        BigInteger,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    event_metadata: Mapped[dict | None] = mapped_column(
        "metadata",
        JSON,
    )

    user = relationship(
        "User",
        back_populates="timeline",
    )