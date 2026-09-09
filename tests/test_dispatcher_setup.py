from types import SimpleNamespace
from unittest import TestCase

from app.middlewares.database import DatabaseMiddleware
from app.middlewares.error import ErrorMiddleware
from app.middlewares.message_persistence import MessagePersistenceMiddleware
from main import configure_middlewares


class MiddlewareRecorder:
    def __init__(self) -> None:
        self.inner = []
        self.outer = []

    def middleware(self, middleware) -> None:
        self.inner.append(middleware)

    def outer_middleware(self, middleware) -> None:
        self.outer.append(middleware)


class DispatcherSetupTest(TestCase):
    def test_message_persistence_runs_before_handler_filtering(self):
        dispatcher = SimpleNamespace(
            update=MiddlewareRecorder(),
            message=MiddlewareRecorder(),
            edited_message=MiddlewareRecorder(),
            chat_member=MiddlewareRecorder(),
            callback_query=MiddlewareRecorder(),
        )

        configure_middlewares(dispatcher)

        self.assertEqual(
            [type(item) for item in dispatcher.message.outer],
            [DatabaseMiddleware, MessagePersistenceMiddleware],
        )
        self.assertEqual(
            [type(item) for item in dispatcher.edited_message.outer],
            [DatabaseMiddleware, MessagePersistenceMiddleware],
        )
        self.assertEqual(
            [type(item) for item in dispatcher.update.inner],
            [ErrorMiddleware],
        )
        self.assertEqual(
            [type(item) for item in dispatcher.callback_query.inner],
            [DatabaseMiddleware],
        )
