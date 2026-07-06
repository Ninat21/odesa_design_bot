from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class SavedMessage(Base, TimestampMixin):
    __tablename__ = "saved_messages"

    __table_args__ = (
        UniqueConstraint(
            "message_id",
            "saved_by",
            "bookmark_type",
            name="uq_saved_messages",
        ),
        Index("ix_saved_messages_message_id", "message_id"),
        Index("ix_saved_messages_saved_by", "saved_by"),
        Index("ix_saved_messages_status", "status"),
        Index("ix_saved_messages_source", "source"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    message_id: Mapped[int] = mapped_column(
        ForeignKey("messages.id"),
        nullable=False,
    )

    saved_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    bookmark_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    note: Mapped[str | None] = mapped_column(
        Text,
    )

    source: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    message = relationship(
        "Message",
        back_populates="saved_by",
    )

    user = relationship(
        "User",
        back_populates="saved_messages",
    )