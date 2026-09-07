from types import SimpleNamespace
from unittest import TestCase

from app.services.message_processor.dto.from_telethon import get_content_type


class TelethonContentTypeTest(TestCase):
    def test_plain_message_is_text(self):
        self.assertEqual(get_content_type(SimpleNamespace()), "text")

    def test_photo_is_detected(self):
        self.assertEqual(
            get_content_type(SimpleNamespace(photo=object())),
            "photo",
        )

    def test_sticker_wins_over_generic_document(self):
        message = SimpleNamespace(sticker=object(), document=object())
        self.assertEqual(get_content_type(message), "sticker")

    def test_animation_wins_over_generic_document(self):
        message = SimpleNamespace(gif=object(), document=object())
        self.assertEqual(get_content_type(message), "animation")
