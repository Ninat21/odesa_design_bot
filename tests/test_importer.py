from unittest import TestCase

from app.services.importer import parse_text, parse_user_id


class ImporterParserTest(TestCase):
    def test_parse_rich_text(self):
        value = ["Hello ", {"type": "bold", "text": "world"}, 10]
        self.assertEqual(parse_text(value), "Hello world")

    def test_parse_user_id(self):
        self.assertEqual(parse_user_id("user123"), 123)
        self.assertIsNone(parse_user_id("channel123"))
        self.assertIsNone(parse_user_id(None))
