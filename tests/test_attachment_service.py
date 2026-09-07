from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from app.services.attachment_service import AttachmentService


def telegram_message(**overrides):
    values = {
        "photo": None,
        "document": None,
        "video": None,
        "audio": None,
        "voice": None,
        "animation": None,
        "video_note": None,
        "sticker": None,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


class AttachmentServiceTest(IsolatedAsyncioTestCase):
    async def test_message_without_attachment_is_ignored(self):
        repository = SimpleNamespace(create_if_missing=AsyncMock())

        await AttachmentService(repository).save_attachments(
            telegram_message(),
            SimpleNamespace(id=10),
        )

        repository.create_if_missing.assert_not_awaited()

    async def test_largest_photo_is_saved_idempotently(self):
        small = SimpleNamespace(
            file_id="small",
            file_unique_id="photo-1",
            file_size=100,
            width=100,
            height=100,
        )
        large = SimpleNamespace(
            file_id="large",
            file_unique_id="photo-1",
            file_size=500,
            width=800,
            height=600,
        )
        repository = SimpleNamespace(create_if_missing=AsyncMock())

        await AttachmentService(repository).save_attachments(
            telegram_message(photo=[small, large]),
            SimpleNamespace(id=10),
        )

        repository.create_if_missing.assert_awaited_once_with(
            message_id=10,
            attachment_type="photo",
            telegram_file_id="large",
            telegram_unique_file_id="photo-1",
            file_size=500,
            width=800,
            height=600,
        )
