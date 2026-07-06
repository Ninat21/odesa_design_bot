from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class EventParticipant(Base, TimestampMixin):
    __tablename__ = "event_participants"

    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "user_id",
            name="uq_event_participant",
        ),
        Index("ix_event_participants_event_id", "event_id"),
        Index("ix_event_participants_user_id", "user_id"),
        Index("ix_event_participants_status", "status"),
        Index("ix_event_participants_registered_at", "registered_at"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    external_participant_id: Mapped[str | None] = mapped_column(
        String(255),
    )

    registration_method: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    consent_personal_data: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    consent_marketing: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    consent_photo: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    checked_in_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    checked_in_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    ticket_type: Mapped[str | None] = mapped_column(
        String(100),
    )

    registered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    event = relationship(
        "Event",
        back_populates="participants",
    )

    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="event_participants",
    )

    checked_in_by_user = relationship(
        "User",
        foreign_keys=[checked_in_by],
        back_populates="checked_in_events",
    )