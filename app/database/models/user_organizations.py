from datetime import date

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class UserOrganization(Base, TimestampMixin):
    __tablename__ = "user_organizations"

    __table_args__ = (
        Index("ix_user_organizations_user_id", "user_id"),
        Index("ix_user_organizations_organization_id", "organization_id"),
        Index("ix_user_organizations_is_current", "is_current"),
        Index("ix_user_organizations_started_at", "started_at"),
        Index("ix_user_organizations_ended_at", "ended_at"),
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

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
    )

    position: Mapped[str | None] = mapped_column(
        String(255),
    )

    department: Mapped[str | None] = mapped_column(
        String(255),
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(100),
    )

    started_at: Mapped[date | None] = mapped_column(
        Date,
    )

    ended_at: Mapped[date | None] = mapped_column(
        Date,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    source: Mapped[str | None] = mapped_column(
        String(100),
    )

    user = relationship(
        "User",
        back_populates="organizations",
    )

    organization = relationship(
        "Organization",
        back_populates="users",
    )