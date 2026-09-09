from types import SimpleNamespace
from unittest import TestCase

from app.handlers.admin.profiles import profile_fact_keyboard, render_profile_card


class ProfileCardTest(TestCase):
    def setUp(self):
        self.user = SimpleNamespace(
            is_member=True,
            username="member",
            first_name="Member",
            last_name=None,
            telegram_id=7,
        )

    def test_facts_are_numbered_and_escaped(self):
        fact = SimpleNamespace(
            id=42,
            fact_type="profession",
            value="UI <designer>",
            verified=False,
            inferred=False,
            confidence=0.9,
        )

        text = render_profile_card(self.user, None, [(fact, None)])

        self.assertIn("1. 📝", text)
        self.assertIn("UI &lt;designer&gt;", text)

    def test_fact_keyboard_targets_fact_id(self):
        fact = SimpleNamespace(id=42)

        keyboard = profile_fact_keyboard([(fact, None)])

        self.assertEqual(
            [button.callback_data for button in keyboard.inline_keyboard[0]],
            ["pf:verify:42", "pf:edit:42", "pf:delete:42"],
        )

    def test_empty_fact_list_has_no_keyboard(self):
        self.assertIsNone(profile_fact_keyboard([]))
