import os
import secrets
from datetime import UTC, datetime
from unittest import IsolatedAsyncioTestCase, skipUnless

from sqlalchemy import delete, func, inspect, select, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import app.database.models  # noqa: F401
from app.database.database import Base
from app.database.models import Message, MessageAttachment, User
from app.database.repositories.message_attachments import (
    MessageAttachmentRepository,
)
from app.database.repositories.messages import MessageRepository
from app.database.repositories.users import UserRepository
from app.services.importer import synchronize_user_statistics

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


@skipUnless(TEST_DATABASE_URL, "TEST_DATABASE_URL is not configured")
class DatabaseIntegrationTest(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.engine = create_async_engine(TEST_DATABASE_URL, pool_pre_ping=True)
        self.sessions = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
        )
        self.telegram_id = 9_000_000_000 + secrets.randbelow(999_999_999)
        self.chat_id = -(8_000_000_000 + secrets.randbelow(999_999_999))

    async def asyncTearDown(self) -> None:
        async with self.sessions() as session:
            await session.execute(
                delete(MessageAttachment).where(
                    MessageAttachment.message_id.in_(
                        select(Message.id).where(Message.chat_id == self.chat_id)
                    )
                )
            )
            await session.execute(
                delete(Message).where(Message.chat_id == self.chat_id)
            )
            await session.execute(
                delete(User).where(User.telegram_id == self.telegram_id)
            )
            await session.commit()
        await self.engine.dispose()

    async def test_schema_matches_models_and_alembic_head(self) -> None:
        def inspect_schema(connection):
            inspector = inspect(connection)
            database_columns = {
                table_name: {
                    column["name"] for column in inspector.get_columns(table_name)
                }
                for table_name in Base.metadata.tables
            }
            version = connection.execute(
                text("SELECT version_num FROM alembic_version")
            ).scalar_one()
            return database_columns, version

        async with self.engine.connect() as connection:
            database_columns, version = await connection.run_sync(inspect_schema)

        for table_name, table in Base.metadata.tables.items():
            self.assertEqual(
                database_columns[table_name],
                set(table.columns.keys()),
                f"Schema drift detected in {table_name}",
            )
        self.assertEqual(version, "a62f1bf37d4c")

    async def test_message_insert_is_idempotent_and_counts_once(self) -> None:
        async with self.sessions() as session:
            users = UserRepository(session)
            messages = MessageRepository(session)
            attachments = MessageAttachmentRepository(session)
            user = await users.upsert_by_telegram_id(
                telegram_id=self.telegram_id,
                username="integration_user",
                first_name="Integration",
                last_name="Test",
                is_bot=False,
                language_code="uk",
                is_premium=False,
            )
            values = {
                "telegram_message_id": 101,
                "user_id": user.id,
                "chat_id": self.chat_id,
                "message_type": "text",
                "text": "Hello",
                "telegram_date": datetime.now(UTC),
            }

            first, first_created = await messages.create_if_missing(**values)
            if first_created:
                await users.record_message_activity(
                    user=user,
                    message_date=values["telegram_date"],
                    is_reply=False,
                    has_media=False,
                )
            second, second_created = await messages.create_if_missing(**values)
            attachment_values = {
                "message_id": first.id,
                "attachment_type": "photo",
                "telegram_file_id": "telegram-file-id",
                "telegram_unique_file_id": "telegram-unique-file-id",
            }
            first_attachment = await attachments.create_if_missing(
                **attachment_values
            )
            second_attachment = await attachments.create_if_missing(
                **attachment_values
            )
            await session.commit()

            self.assertTrue(first_created)
            self.assertFalse(second_created)
            self.assertEqual(first.id, second.id)
            self.assertEqual(first_attachment.id, second_attachment.id)

        async with self.sessions() as session:
            message_count = await session.scalar(
                select(func.count()).select_from(Message).where(
                    Message.chat_id == self.chat_id
                )
            )
            attachment_count = await session.scalar(
                select(func.count()).select_from(MessageAttachment).where(
                    MessageAttachment.message_id == first.id
                )
            )
            user = await session.scalar(
                select(User).where(User.telegram_id == self.telegram_id)
            )

        self.assertEqual(message_count, 1)
        self.assertEqual(attachment_count, 1)
        self.assertEqual(user.messages_count, 1)

    async def test_rollback_removes_uncommitted_changes(self) -> None:
        async with self.sessions() as session:
            users = UserRepository(session)
            await users.upsert_by_telegram_id(
                telegram_id=self.telegram_id,
                username=None,
                first_name="Rollback",
                last_name=None,
                is_bot=False,
                language_code=None,
                is_premium=False,
            )
            await session.rollback()

        async with self.sessions() as session:
            user = await session.scalar(
                select(User).where(User.telegram_id == self.telegram_id)
            )

        self.assertIsNone(user)

    async def test_import_statistics_are_synchronized(self) -> None:
        async with self.sessions() as session:
            users = UserRepository(session)
            messages = MessageRepository(session)
            user = await users.upsert_by_telegram_id(
                telegram_id=self.telegram_id,
                username=None,
                first_name="Imported",
                last_name=None,
                is_bot=False,
                language_code=None,
                is_premium=False,
            )
            first, _ = await messages.create_if_missing(
                telegram_message_id=201,
                user_id=user.id,
                chat_id=self.chat_id,
                message_type="text",
                text="First",
                telegram_date=datetime(2026, 9, 6, tzinfo=UTC),
            )
            await messages.create_if_missing(
                telegram_message_id=202,
                user_id=user.id,
                chat_id=self.chat_id,
                message_type="photo",
                text=None,
                telegram_date=datetime(2026, 9, 7, tzinfo=UTC),
                reply_to_message_id=first.id,
            )

            await synchronize_user_statistics(session, [user.id])
            await session.commit()

        async with self.sessions() as session:
            user = await session.scalar(
                select(User).where(User.telegram_id == self.telegram_id)
            )

        self.assertEqual(user.messages_count, 2)
        self.assertEqual(user.replies_count, 1)
        self.assertEqual(user.media_count, 1)
        self.assertEqual(user.last_message_at, datetime(2026, 9, 7, tzinfo=UTC))

    async def test_membership_dates_are_persisted(self) -> None:
        joined_at = datetime(2026, 8, 1, tzinfo=UTC)
        left_at = datetime(2026, 9, 1, tzinfo=UTC)

        async with self.sessions() as session:
            users = UserRepository(session)
            user = await users.upsert_by_telegram_id(
                telegram_id=self.telegram_id,
                username=None,
                first_name="Member",
                last_name=None,
                is_bot=False,
                language_code=None,
                is_premium=False,
            )
            await users.mark_joined(user, joined_at)
            await users.mark_left(user, left_at)
            observed_at = datetime(2026, 9, 2, tzinfo=UTC)
            await users.mark_present(user, observed_at)
            await session.commit()

        async with self.sessions() as session:
            user = await session.scalar(
                select(User).where(User.telegram_id == self.telegram_id)
            )

        self.assertTrue(user.is_member)
        self.assertEqual(user.joined_at, joined_at)
        self.assertIsNone(user.left_at)
        self.assertEqual(user.last_seen_at, observed_at)
