from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class KnowledgeArticle(Base, TimestampMixin):
    __tablename__ = "knowledge_articles"

    __table_args__ = (
        UniqueConstraint(
            "slug",
            name="uq_knowledge_articles_slug",
        ),
        Index("ix_knowledge_articles_slug", "slug"),
        Index("ix_knowledge_articles_status", "status"),
        Index("ix_knowledge_articles_published_at", "published_at"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    author_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    source: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    author = relationship(
        "User",
        back_populates="knowledge_articles",
    )

    sources = relationship(
        "KnowledgeSource",
        back_populates="article",
    )

    tags = relationship(
        "KnowledgeTag",
        back_populates="article",
    )