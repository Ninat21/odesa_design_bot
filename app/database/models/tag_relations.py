from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Index,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class TagRelation(Base, TimestampMixin):
    __tablename__ = "tag_relations"

    __table_args__ = (
        Index("ix_tag_relations_tag_id", "tag_id"),
        Index("ix_tag_relations_entity_type", "entity_type"),
        Index("ix_tag_relations_entity_id", "entity_id"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id"),
        nullable=False,
    )

    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    entity_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    tag = relationship(
        "Tag",
        back_populates="relations",
    )