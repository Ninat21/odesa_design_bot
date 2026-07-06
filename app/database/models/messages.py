from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    __table_args__ = (
        UniqueConstraint(
            "chat_id",
            "telegram_message_id",
            name="uq_messages_chat_message",
        ),
        Index("ix_messages_user_id", "user_id"),
        Index("ix_messages_chat_id", "chat_id"),
        Index("ix_messages_telegram_date", "telegram_date"),
        Index("ix_messages_message_type", "message_type"),
        Index("ix_messages_reply_to_message_id", "reply_to_message_id"),
        Index("ix_messages_thread_id", "thread_id"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    telegram_message_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    telegram_chat_type: Mapped[str | None] = mapped_column(
        String(30),
    )

    telegram_chat_title: Mapped[str | None] = mapped_column(
        String(255),
    )

    telegram_chat_username: Mapped[str | None] = mapped_column(
        String(255),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    chat_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    thread_id: Mapped[int | None] = mapped_column(
        BigInteger,
    )

    media_group_id: Mapped[str | None] = mapped_column(
        String(255),
    )

    reply_to_message_id: Mapped[int | None] = mapped_column(
        ForeignKey("messages.id"),
    )

    forwarded_from_user_id: Mapped[int | None] = mapped_column(
        BigInteger,
    )

    forwarded_chat_id: Mapped[int | None] = mapped_column(
        BigInteger,
    )

    sender_chat_id: Mapped[int | None] = mapped_column(
        BigInteger,
    )

    via_bot_id: Mapped[int | None] = mapped_column(
        BigInteger,
    )

    message_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    text: Mapped[str | None] = mapped_column(
        Text,
    )

    caption: Mapped[str | None] = mapped_column(
        Text,
    )

    entities_json: Mapped[str | None] = mapped_column(
        Text,
    )

    caption_entities_json: Mapped[str | None] = mapped_column(
        Text,
    )

        
    forward_origin_json: Mapped[str | None] = mapped_column(
        Text,
    )

    external_reply_json: Mapped[str | None] = mapped_column(
        Text,
    )

    quote_json: Mapped[str | None] = mapped_column(
        Text,
    )

    link_preview_json: Mapped[str | None] = mapped_column(
        Text,
    )

    telegram_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    edited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    is_topic_message: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    has_media_spoiler: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    views_count: Mapped[int | None] = mapped_column(
        Integer,
    )

    forwards_count: Mapped[int | None] = mapped_column(
        Integer,
    )

    effect_id: Mapped[str | None] = mapped_column(
        String(255),
    )

    business_connection_id: Mapped[str | None] = mapped_column(
        String(255),
    )    

    is_deleted: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="messages",
    )

    reply_to_message = relationship(
        "Message",
        remote_side=[id],
        back_populates="replies",
    )

    replies = relationship(
        "Message",
        back_populates="reply_to_message",
    )

    attachments = relationship(
        "MessageAttachment",
        back_populates="message",
    )

    saved_by = relationship(
        "SavedMessage",
        back_populates="message",
    )

