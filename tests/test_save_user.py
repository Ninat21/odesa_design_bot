from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from app.services.message_processor.steps.save_user import SaveUserStep


class SaveUserStepTest(IsolatedAsyncioTestCase):
    async def test_optional_premium_flag_is_normalized_to_boolean(self):
        repository = SimpleNamespace(upsert_by_telegram_id=AsyncMock())
        step = SaveUserStep(repository)
        telegram_user = SimpleNamespace(
            id=1,
            username="member",
            first_name="Member",
            last_name=None,
            is_bot=False,
            language_code="uk",
            is_premium=None,
        )

        await step.execute(telegram_user)

        repository.upsert_by_telegram_id.assert_awaited_once_with(
            telegram_id=1,
            username="member",
            first_name="Member",
            last_name=None,
            is_bot=False,
            language_code="uk",
            is_premium=False,
        )
