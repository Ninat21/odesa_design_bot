"""Add sourced facts for user profile cards.

Revision ID: c91d38a72f44
Revises: a62f1bf37d4c
Create Date: 2026-09-08
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c91d38a72f44"
down_revision: str | None = "a62f1bf37d4c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "profile_facts",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("fact_type", sa.String(length=50), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("source_type", sa.String(length=30), nullable=False),
        sa.Column("source_key", sa.String(length=255), nullable=False),
        sa.Column("source_message_id", sa.BigInteger(), nullable=True),
        sa.Column("confidence", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("verified", sa.Boolean(), nullable=False),
        sa.Column("inferred", sa.Boolean(), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["source_message_id"], ["messages.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "fact_type",
            "value",
            "source_key",
            name="uq_profile_fact_source",
        ),
    )
    op.create_index(
        "ix_profile_facts_fact_type",
        "profile_facts",
        ["fact_type"],
        unique=False,
    )
    op.create_index(
        "ix_profile_facts_user_id",
        "profile_facts",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_profile_facts_verified",
        "profile_facts",
        ["verified"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_profile_facts_verified", table_name="profile_facts")
    op.drop_index("ix_profile_facts_user_id", table_name="profile_facts")
    op.drop_index("ix_profile_facts_fact_type", table_name="profile_facts")
    op.drop_table("profile_facts")
