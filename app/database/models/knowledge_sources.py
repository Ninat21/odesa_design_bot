from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Index,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class KnowledgeSource(Base, TimestampMixin):
    __tablename__ = "knowledge_sources"

    __table_args__ = (
        Index(
            "ix_knowledge_sources_article_id",
            "knowledge_article_id",
        ),
        Index(
            "ix_knowledge_sources_source_type",
            "source_type",
        ),
        Index(
            "ix_knowledge_sources_source_id",
            "source_id",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    knowledge_article_id: Mapped[int] = mapped_column(
        ForeignKey("knowledge_articles.id"),
        nullable=False,
    )

    source_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    source_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    article = relationship(
        "KnowledgeArticle",
        back_populates="sources",
    )