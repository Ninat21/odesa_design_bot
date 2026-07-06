from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models.base import TimestampMixin


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_log"

    __table_args__ = (
        Index("ix_audit_log_entity_type", "entity_type"),
        Index("ix_audit_log_entity_id", "entity_id"),
        Index("ix_audit_log_action", "action"),
        Index("ix_audit_log_changed_by", "changed_by"),
        Index("ix_audit_log_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    entity_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    field_name: Mapped[str | None] = mapped_column(
        String(100),
    )

    old_value: Mapped[str | None] = mapped_column(
        Text,
    )

    new_value: Mapped[str | None] = mapped_column(
        Text,
    )

    changed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    source: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
    )

    changed_by_user = relationship(
        "User",
        foreign_keys=[changed_by],
        back_populates="audit_logs",
    )