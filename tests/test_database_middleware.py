from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from app.middlewares.database import DatabaseMiddleware


class SessionContext:
    def __init__(self, session):
        self.session = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, *_args):
        return None


class DatabaseMiddlewareTest(IsolatedAsyncioTestCase):
    async def test_success_commits_transaction(self):
        session = SimpleNamespace(
            commit=AsyncMock(),
            rollback=AsyncMock(),
        )
        handler = AsyncMock(return_value="handled")
        data = {}

        with patch(
            "app.middlewares.database.SessionLocal",
            return_value=SessionContext(session),
        ):
            result = await DatabaseMiddleware()(handler, object(), data)

        self.assertEqual(result, "handled")
        session.commit.assert_awaited_once_with()
        session.rollback.assert_not_awaited()
        self.assertIn("services", data)

    async def test_failure_rolls_back_and_propagates(self):
        session = SimpleNamespace(
            commit=AsyncMock(),
            rollback=AsyncMock(),
        )
        handler = AsyncMock(side_effect=ValueError("failed"))

        with patch(
            "app.middlewares.database.SessionLocal",
            return_value=SessionContext(session),
        ):
            with self.assertRaisesRegex(ValueError, "failed"):
                await DatabaseMiddleware()(handler, object(), {})

        session.commit.assert_not_awaited()
        session.rollback.assert_awaited_once_with()
