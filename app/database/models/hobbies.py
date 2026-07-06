from sqlalchemy import (
    BigInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class Hobby(Base, TimestampMixin):
    __tablename__ = "hobbies"

    __table_args__ = (
        UniqueConstraint("slug", name="uq_hobbies_slug"),
        UniqueConstraint("name", name="uq_hobbies_name"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    users = relationship(
        "UserHobby",
        back_populates="hobby",
    )