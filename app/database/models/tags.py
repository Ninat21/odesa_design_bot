from sqlalchemy import BigInteger, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    __table_args__ = (
        UniqueConstraint(
            "name",
            name="uq_tags_name",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    color: Mapped[str | None] = mapped_column(
        String(20),
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    relations = relationship(
        "TagRelation",
        back_populates="tag",
    )