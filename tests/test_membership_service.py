from datetime import UTC, datetime
from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from app.services.membership_service import MembershipService


class MembershipServiceTest(IsolatedAsyncioTestCase):
    async def test_join_upserts_user_and_marks_membership(self):
        user = SimpleNamespace(id=10)
        repository = SimpleNamespace(mark_joined=AsyncMock(return_value=user))
        service = MembershipService(repository)
        service.save_user.execute = AsyncMock(return_value=user)
        telegram_user = SimpleNamespace(id=7)
        joined_at = datetime(2026, 9, 7, tzinfo=UTC)

        result = await service.join(telegram_user, joined_at)

        self.assertIs(result, user)
        service.save_user.execute.assert_awaited_once_with(telegram_user)
        repository.mark_joined.assert_awaited_once_with(user, joined_at)

    async def test_leave_upserts_user_and_marks_membership(self):
        user = SimpleNamespace(id=10)
        repository = SimpleNamespace(mark_left=AsyncMock(return_value=user))
        service = MembershipService(repository)
        service.save_user.execute = AsyncMock(return_value=user)
        telegram_user = SimpleNamespace(id=7)
        left_at = datetime(2026, 9, 7, tzinfo=UTC)

        result = await service.leave(telegram_user, left_at)

        self.assertIs(result, user)
        service.save_user.execute.assert_awaited_once_with(telegram_user)
        repository.mark_left.assert_awaited_once_with(user, left_at)
