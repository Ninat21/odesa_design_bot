from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    __table_args__ = (
        UniqueConstraint(
            "source",
            "external_id",
            name="uq_events_source_external_id",
        ),
        UniqueConstraint(
            "slug",
            name="uq_events_slug",
        ),
        Index("ix_events_starts_at", "starts_at"),
        Index("ix_events_status", "status"),
        Index("ix_events_event_type", "event_type"),
        Index("ix_events_city", "city"),
        Index("ix_events_source", "source"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    external_id: Mapped[str | None] = mapped_column(
        String(255),
    )

    source: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str | None] = mapped_column(
        String(255),
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    organizer_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    venue_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    address: Mapped[str | None] = mapped_column(
        Text,
    )

    city: Mapped[str | None] = mapped_column(
        String(255),
    )

    country: Mapped[str | None] = mapped_column(
        String(255),
    )

    latitude: Mapped[float | None] = mapped_column(
        Numeric(9, 6),
    )

    longitude: Mapped[float | None] = mapped_column(
        Numeric(9, 6),
    )

    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    ends_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    registration_url: Mapped[str | None] = mapped_column(
        Text,
    )

    cover_image_url: Mapped[str | None] = mapped_column(
        Text,
    )

    max_participants: Mapped[int | None] = mapped_column(
        Integer,
    )

    participants = relationship(
        "EventParticipant",
        back_populates="event",
    )

    feedback = relationship(
        "EventFeedback",
        back_populates="event",
    )