from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class KnowledgeTag(Base, TimestampMixin):
    __tablename__ = "knowledge_tags"

    __table_args__ = (
        UniqueConstraint(
            "knowledge_article_id",
            "tag_name",
            name="uq_knowledge_article_tag",
        ),
        Index("ix_knowledge_tags_tag", "tag_name"),
        Index(
            "ix_knowledge_tags_article_id",
            "knowledge_article_id",
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

    tag_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    article = relationship(
        "KnowledgeArticle",
        back_populates="tags",
    )