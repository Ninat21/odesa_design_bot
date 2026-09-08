from unittest import TestCase

from app.bot_commands import (
    ADMIN_COMMANDS,
    PUBLIC_COMMANDS,
    command_help_text,
)


class BotCommandsTest(TestCase):
    def test_command_names_are_unique(self):
        names = [command for command, _ in PUBLIC_COMMANDS + ADMIN_COMMANDS]
        self.assertEqual(len(names), len(set(names)))

    def test_public_help_does_not_expose_admin_commands(self):
        text = command_help_text(is_admin=False)
        self.assertIn("/help", text)
        self.assertIn("/ping", text)
        self.assertNotIn("/members", text)

    def test_admin_help_contains_all_commands(self):
        text = command_help_text(is_admin=True)
        for command, _ in PUBLIC_COMMANDS + ADMIN_COMMANDS:
            self.assertIn(f"/{command}", text)
