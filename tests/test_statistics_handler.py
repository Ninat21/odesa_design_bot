from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock

from app.handlers.admin.statistics import answer_html, user_link


class UserLinkTest(TestCase):
    def test_username_is_escaped(self):
        user = SimpleNamespace(
            username="name<tag>",
            first_name=None,
            telegram_id=7,
        )
        self.assertEqual(user_link(user), "@name&lt;tag&gt;")

    def test_name_is_escaped(self):
        user = SimpleNamespace(
            username=None,
            first_name="<Name>",
            telegram_id=7,
        )
        self.assertEqual(
            user_link(user),
            '<a href="tg://user?id=7">&lt;Name&gt;</a>',
        )


class AnswerHtmlTest(IsolatedAsyncioTestCase):
    async def test_long_answer_is_split_at_line_boundaries(self):
        message = SimpleNamespace(answer=AsyncMock())
        text = f"{'a' * 3_000}\n{'b' * 3_000}\n"

        await answer_html(message, text)

        self.assertEqual(message.answer.await_count, 2)
        for call in message.answer.await_args_list:
            self.assertLessEqual(len(call.args[0]), 4_000)
            self.assertEqual(call.kwargs["parse_mode"], "HTML")
