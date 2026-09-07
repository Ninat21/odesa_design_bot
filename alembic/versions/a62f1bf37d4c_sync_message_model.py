"""Synchronize the messages table with the ORM model.

Revision ID: a62f1bf37d4c
Revises: e27eb129e081
Create Date: 2026-09-07
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "a62f1bf37d4c"
down_revision: str | None = "e27eb129e081"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    existing_columns = {
        column["name"] for column in inspector.get_columns("messages")
    }
    columns = [
        sa.Column("telegram_chat_type", sa.String(30)),
        sa.Column("telegram_chat_title", sa.String(255)),
        sa.Column("telegram_chat_username", sa.String(255)),
        sa.Column("media_group_id", sa.String(255)),
        sa.Column("sender_chat_id", sa.BigInteger()),
        sa.Column("via_bot_id", sa.BigInteger()),
        sa.Column("entities_json", sa.Text()),
        sa.Column("caption_entities_json", sa.Text()),
        sa.Column("forward_origin_json", sa.Text()),
        sa.Column("external_reply_json", sa.Text()),
        sa.Column("quote_json", sa.Text()),
        sa.Column("link_preview_json", sa.Text()),
        sa.Column(
            "is_topic_message",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "has_media_spoiler",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("effect_id", sa.String(255)),
        sa.Column("business_connection_id", sa.String(255)),
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    ]

    added_columns: set[str] = set()
    for column in columns:
        if column.name not in existing_columns:
            op.add_column("messages", column)
            added_columns.add(column.name)

    for column_name in {
        "is_topic_message",
        "has_media_spoiler",
        "is_deleted",
    } & added_columns:
        op.alter_column("messages", column_name, server_default=None)

    unique_constraints = inspector.get_unique_constraints("message_attachments")
    attachment_key = {"message_id", "telegram_unique_file_id"}
    has_attachment_constraint = any(
        set(constraint.get("column_names") or []) == attachment_key
        for constraint in unique_constraints
    )

    if not has_attachment_constraint:
        op.create_unique_constraint(
            "uq_message_attachments_message_file",
            "message_attachments",
            ["message_id", "telegram_unique_file_id"],
        )


def downgrade() -> None:
    op.drop_constraint(
        "uq_message_attachments_message_file",
        "message_attachments",
        type_="unique",
    )
    op.drop_column("messages", "is_deleted")
    op.drop_column("messages", "business_connection_id")
    op.drop_column("messages", "effect_id")
    op.drop_column("messages", "has_media_spoiler")
    op.drop_column("messages", "is_topic_message")
    op.drop_column("messages", "link_preview_json")
    op.drop_column("messages", "quote_json")
    op.drop_column("messages", "external_reply_json")
    op.drop_column("messages", "forward_origin_json")
    op.drop_column("messages", "caption_entities_json")
    op.drop_column("messages", "entities_json")
    op.drop_column("messages", "via_bot_id")
    op.drop_column("messages", "sender_chat_id")
    op.drop_column("messages", "media_group_id")
    op.drop_column("messages", "telegram_chat_username")
    op.drop_column("messages", "telegram_chat_title")
    op.drop_column("messages", "telegram_chat_type")
