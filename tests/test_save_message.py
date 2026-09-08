from datetime import UTC, datetime
from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from app.services.message_processor.dto.from_aiogram import from_aiogram
from app.services.message_processor.dto.telegram_message import TelegramMessageDTO
from app.services.message_processor.steps.save_message import SaveMessageStep


def make_message(**overrides) -> TelegramMessageDTO:
    values = {
        "telegram_message_id": 100,
        "chat_id": -1001,
        "chat_type": "supergroup",
        "chat_title": "Community",
        "chat_username": None,
        "user_id": 42,
        "text": "Hello",
        "caption": None,
        "content_type": "text",
        "date": datetime(2026, 9, 7, tzinfo=UTC),
        "edit_date": None,
        "reply_to_message_id": None,
        "thread_id": None,
        "media_group_id": None,
        "sender_chat_id": None,
        "via_bot_id": None,
        "entities": None,
        "caption_entities": None,
        "forward_origin": None,
        "external_reply": None,
        "quote": None,
        "link_preview": None,
        "has_media_spoiler": False,
        "is_topic_message": False,
        "effect_id": None,
        "business_connection_id": None,
    }
    values.update(overrides)
    return TelegramMessageDTO(**values)


def make_user():
    return SimpleNamespace(
        id=7,
        messages_count=0,
        replies_count=0,
        media_count=0,
        last_message_at=None,
        last_activity_at=None,
    )


class SaveMessageStepTest(IsolatedAsyncioTestCase):
    async def test_duplicate_is_idempotent(self):
        existing = SimpleNamespace(id=9)
        messages = SimpleNamespace(
            create_if_missing=AsyncMock(return_value=(existing, False)),
        )
        users = SimpleNamespace(record_message_activity=AsyncMock())
        user = make_user()

        result = await SaveMessageStep(messages, users).execute(
            make_message(),
            user,
        )

        self.assertIs(result, existing)
        self.assertEqual(user.messages_count, 0)
        messages.create_if_missing.assert_awaited_once()
        users.record_message_activity.assert_not_awaited()

    async def test_new_message_is_created_and_updates_counters(self):
        created = SimpleNamespace(id=10)
        messages = SimpleNamespace(
            create_if_missing=AsyncMock(return_value=(created, True)),
        )
        users = SimpleNamespace(record_message_activity=AsyncMock())
        user = make_user()
        dto = make_message(content_type="photo", reply_to_message_id=88)

        result = await SaveMessageStep(messages, users).execute(
            dto,
            user,
            reply_to_message_id=5,
        )

        self.assertIs(result, created)
        self.assertEqual(
            messages.create_if_missing.await_args.kwargs["reply_to_message_id"],
            5,
        )
        users.record_message_activity.assert_awaited_once_with(
            user=user,
            message_date=dto.date,
            is_reply=True,
            has_media=True,
        )


class AiogramMessageConversionTest(IsolatedAsyncioTestCase):
    async def test_nullable_telegram_booleans_are_normalized(self):
        message = SimpleNamespace(
            message_id=1,
            chat=SimpleNamespace(
                id=-1001,
                type="supergroup",
                title="Community",
                username=None,
            ),
            from_user=SimpleNamespace(id=42),
            text=None,
            caption=None,
            content_type="new_chat_members",
            date=datetime(2026, 9, 8, tzinfo=UTC),
            edit_date=None,
            reply_to_message=None,
            message_thread_id=None,
            media_group_id=None,
            sender_chat=None,
            via_bot=None,
            entities=None,
            caption_entities=None,
            forward_origin=None,
            external_reply=None,
            quote=None,
            link_preview_options=None,
            has_media_spoiler=None,
            is_topic_message=None,
            effect_id=None,
            business_connection_id=None,
        )

        dto = from_aiogram(message)

        self.assertFalse(dto.has_media_spoiler)
        self.assertFalse(dto.is_topic_message)
