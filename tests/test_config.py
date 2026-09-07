import os
from unittest import TestCase, mock

from app.config import required_int_list


class RequiredIntListTest(TestCase):
    def test_parses_comma_separated_ids(self):
        with mock.patch.dict(os.environ, {"TEST_IDS": "123, 456"}):
            self.assertEqual(required_int_list("TEST_IDS"), (123, 456))

    def test_rejects_invalid_id(self):
        with mock.patch.dict(os.environ, {"TEST_IDS": "123,not-an-id"}):
            with self.assertRaisesRegex(RuntimeError, "розділені комами"):
                required_int_list("TEST_IDS")
