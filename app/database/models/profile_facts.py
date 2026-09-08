from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class ProfileFact(Base, TimestampMixin):
    __tablename__ = "profile_facts"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "fact_type",
            "value",
            "source_key",
            name="uq_profile_fact_source",
        ),
        Index("ix_profile_facts_user_id", "user_id"),
        Index("ix_profile_facts_fact_type", "fact_type"),
        Index("ix_profile_facts_verified", "verified"),
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
    fact_type: Mapped[str] = mapped_column(String(50), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    source_type: Mapped[str] = mapped_column(String(30), nullable=False)
    source_key: Mapped[str] = mapped_column(String(255), nullable=False)
    source_message_id: Mapped[int | None] = mapped_column(
        ForeignKey("messages.id"),
    )
    confidence: Mapped[float | None] = mapped_column(Numeric(5, 2))
    verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    inferred: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    observed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user = relationship("User", back_populates="profile_facts")
    source_message = relationship("Message")
