from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    __table_args__ = (
        Index("ix_users_telegram_id", "telegram_id"),
        Index("ix_users_username", "username"),
        Index("ix_users_is_member", "is_member"),
        Index("ix_users_last_activity_at", "last_activity_at"),
        Index("ix_users_last_message_at", "last_message_at"),
    )

    id: Mapped[int] = mapped_column(
    BigInteger,
    primary_key=True,
    autoincrement=True,
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
    )

    username: Mapped[str | None] = mapped_column(
        String(255),
    )

    first_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    last_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    language_code: Mapped[str | None] = mapped_column(
        String(10),
    )

    is_bot: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_premium: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_member: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_banned: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    joined_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    left_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    first_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    last_activity_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    last_message_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    messages_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    media_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    replies_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
    )

    organizations = relationship(
        "UserOrganization",
        back_populates="user",
    )

    skills = relationship(
        "UserSkill",
        back_populates="user",
    )

    interests = relationship(
        "UserInterest",
        back_populates="user",
    )

    hobbies = relationship(
        "UserHobby",
        back_populates="user",
    )

    ai_profile = relationship(
        "AIProfile",
        back_populates="user",
        uselist=False,
    )

    messages = relationship(
        "Message",
        back_populates="user",
    )

    saved_messages = relationship(
        "SavedMessage",
        back_populates="user",
    )    

    timeline = relationship(
        "Timeline",
        back_populates="user",
    )

    audit_logs = relationship(
        "AuditLog",
        foreign_keys="AuditLog.changed_by",
        back_populates="changed_by_user",
    )

    event_participants = relationship(
        "EventParticipant",
        foreign_keys="EventParticipant.user_id",
        back_populates="user",
    )

    event_feedback = relationship(
        "EventFeedback",
        back_populates="user",
    )

    checked_in_events = relationship(
        "EventParticipant",
        foreign_keys="EventParticipant.checked_in_by",
        back_populates="checked_in_by_user",
    )

    knowledge_articles = relationship(
        "KnowledgeArticle",
        back_populates="author",
    )

    notifications = relationship(
        "Notification",
        back_populates="user",
    )

    
