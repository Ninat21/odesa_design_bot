from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class MessageAttachment(Base, TimestampMixin):
    __tablename__ = "message_attachments"

    __table_args__ = (
        Index("ix_message_attachments_message_id", "message_id"),
        Index("ix_message_attachments_attachment_type", "attachment_type"),
        Index(
            "ix_message_attachments_telegram_unique_file_id",
            "telegram_unique_file_id",
        ),
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

    attachment_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    telegram_file_id: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    telegram_unique_file_id: Mapped[str | None] = mapped_column(
        Text,
    )

    file_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    mime_type: Mapped[str | None] = mapped_column(
        String(100),
    )

    file_size: Mapped[int | None] = mapped_column(
        BigInteger,
    )

    width: Mapped[int | None] = mapped_column(
        Integer,
    )

    height: Mapped[int | None] = mapped_column(
        Integer,
    )

    duration: Mapped[int | None] = mapped_column(
        Integer,
    )

    thumbnail_file_id: Mapped[str | None] = mapped_column(
        Text,
    )

    message = relationship(
        "Message",
        back_populates="attachments",
    )