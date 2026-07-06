from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
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


class Profile(Base, TimestampMixin):
    __tablename__ = "profiles"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            name="uq_profiles_user_id",
        ),
        Index("ix_profiles_user_id", "user_id"),
        Index("ix_profiles_email", "email"),
        Index("ix_profiles_city", "city"),
        Index("ix_profiles_profession", "profession"),
        Index("ix_profiles_company", "company"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    display_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
    )

    birth_date: Mapped[date | None] = mapped_column(
        Date,
    )

    city: Mapped[str | None] = mapped_column(
        String(255),
    )

    country: Mapped[str | None] = mapped_column(
        String(255),
    )

    profession: Mapped[str | None] = mapped_column(
        String(255),
    )

    company: Mapped[str | None] = mapped_column(
        String(255),
    )

    position: Mapped[str | None] = mapped_column(
        String(255),
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
    )

    instagram: Mapped[str | None] = mapped_column(
        String(255),
    )

    behance: Mapped[str | None] = mapped_column(
        String(255),
    )

    linkedin: Mapped[str | None] = mapped_column(
        String(255),
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
    )

    portfolio_url: Mapped[str | None] = mapped_column(
        String(255),
    )

    avatar_url: Mapped[str | None] = mapped_column(
        Text,
    )

    newsletter_consent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    personal_data_consent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    profile_completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    user = relationship(
        "User",
        back_populates="profile",
    )