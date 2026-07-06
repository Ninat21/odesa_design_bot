from sqlalchemy import BigInteger, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class Skill(Base, TimestampMixin):
    __tablename__ = "skills"

    __table_args__ = (
        UniqueConstraint("slug", name="uq_skills_slug"),
        UniqueConstraint("name", name="uq_skills_name"),
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

    category: Mapped[str | None] = mapped_column(
        String(100),
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    users = relationship(
        "UserSkill",
        back_populates="skill",
    )