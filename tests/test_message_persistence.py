from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from app.config import Config
from app.middlewares.message_persistence import MessagePersistenceMiddleware


class MessagePersistenceMiddlewareTest(IsolatedAsyncioTestCase):
    async def test_target_group_message_is_persisted_before_handler(self):
        calls = []

        async def process(**_kwargs):
            calls.append("persist")

        async def commit():
            calls.append("commit")

        async def handler(_event, _data):
            calls.append("handler")
            return "handled"

        event = SimpleNamespace(
            chat=SimpleNamespace(id=-1001),
            from_user=SimpleNamespace(id=7),
        )
        services = SimpleNamespace(
            message_processor=SimpleNamespace(process=process),
        )
        session = SimpleNamespace(commit=commit)

        with patch.object(Config, "GROUP_ID", -1001):
            result = await MessagePersistenceMiddleware()(
                handler,
                event,
                {"services": services, "session": session},
            )

        self.assertEqual(result, "handled")
        self.assertEqual(calls, ["persist", "commit", "handler"])

    async def test_other_chat_is_not_persisted(self):
        handler = AsyncMock(return_value="handled")
        process = AsyncMock()
        event = SimpleNamespace(
            chat=SimpleNamespace(id=-2002),
            from_user=SimpleNamespace(id=7),
        )
        services = SimpleNamespace(
            message_processor=SimpleNamespace(process=process),
        )
        data = {"services": services, "session": SimpleNamespace()}

        with patch.object(Config, "GROUP_ID", -1001):
            result = await MessagePersistenceMiddleware()(
                handler,
                event,
                data,
            )

        self.assertEqual(result, "handled")
        process.assert_not_awaited()
        handler.assert_awaited_once_with(event, data)

    async def test_handler_failure_happens_after_persistence_commit(self):
        process = AsyncMock()
        commit = AsyncMock()
        handler = AsyncMock(side_effect=RuntimeError("Telegram failed"))
        event = SimpleNamespace(
            chat=SimpleNamespace(id=-1001),
            from_user=SimpleNamespace(id=7),
        )
        data = {
            "services": SimpleNamespace(
                message_processor=SimpleNamespace(process=process),
            ),
            "session": SimpleNamespace(commit=commit),
        }

        with patch.object(Config, "GROUP_ID", -1001):
            with self.assertRaisesRegex(RuntimeError, "Telegram failed"):
                await MessagePersistenceMiddleware()(handler, event, data)

        process.assert_awaited_once()
        commit.assert_awaited_once_with()
