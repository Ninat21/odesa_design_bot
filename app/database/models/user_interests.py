from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class UserInterest(Base, TimestampMixin):
    __tablename__ = "user_interests"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "interest_id",
            name="uq_user_interest",
        ),
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

    interest_id: Mapped[int] = mapped_column(
        ForeignKey("interests.id"),
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    confidence: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
    )

    verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="interests",
    )

    interest = relationship(
        "Interest",
        back_populates="users",
    )