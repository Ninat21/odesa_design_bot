from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    Index,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class EventFeedback(Base, TimestampMixin):
    __tablename__ = "event_feedback"

    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "user_id",
            name="uq_event_feedback",
        ),
        Index("ix_event_feedback_event_id", "event_id"),
        Index("ix_event_feedback_user_id", "user_id"),
        Index("ix_event_feedback_rating", "rating"),
        Index("ix_event_feedback_created_at", "created_at"),
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

    rating: Mapped[int | None] = mapped_column(
        SmallInteger,
    )

    review: Mapped[str | None] = mapped_column(
        Text,
    )

    would_recommend: Mapped[bool | None] = mapped_column(
        Boolean,
    )

    source: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    event = relationship(
        "Event",
        back_populates="feedback",
    )

    user = relationship(
        "User",
        back_populates="event_feedback",
    )