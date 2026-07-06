from sqlalchemy import BigInteger, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    __table_args__ = (
        Index("ix_organizations_name", "name"),
        Index("ix_organizations_city", "city"),
        Index("ix_organizations_country", "country"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    legal_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
    )

    linkedin: Mapped[str | None] = mapped_column(
        String(255),
    )

    instagram: Mapped[str | None] = mapped_column(
        String(255),
    )

    city: Mapped[str | None] = mapped_column(
        String(255),
    )

    country: Mapped[str | None] = mapped_column(
        String(255),
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    users = relationship(
        "UserOrganization",
        back_populates="organization",
    )