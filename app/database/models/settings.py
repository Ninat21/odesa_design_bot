from sqlalchemy import BigInteger, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base
from app.database.models.base import TimestampMixin


class Setting(Base, TimestampMixin):
    __tablename__ = "settings"

    __table_args__ = (
        UniqueConstraint(
            "key",
            name="uq_settings_key",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    value: Mapped[str | None] = mapped_column(
        Text,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )