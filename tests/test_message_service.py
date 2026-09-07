from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.message_service import MessageService


class MessageServiceTest(IsolatedAsyncioTestCase):
    async def test_compatibility_service_uses_canonical_pipeline(self):
        processor = MagicMock()
        processor.process = AsyncMock(return_value="stored-message")

        with patch(
            "app.services.message_service.MessageProcessor",
            return_value=processor,
        ):
            service = MessageService(MagicMock(), MagicMock(), MagicMock())

        result = await service.save_message("user", "message")

        self.assertEqual(result, "stored-message")
        processor.process.assert_awaited_once_with(
            telegram_user="user",
            telegram_message="message",
        )
