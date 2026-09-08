from datetime import UTC, datetime
from unittest import TestCase

from app.services.profile_extractor import extract_profile_facts


class ProfileExtractorTest(TestCase):
    def setUp(self):
        self.date = datetime(2026, 9, 8, tzinfo=UTC)

    def test_extracts_explicit_age_with_observation_date(self):
        facts = extract_profile_facts("Мені 27 років", self.date)
        self.assertEqual(facts[0].fact_type, "age")
        self.assertEqual(facts[0].value, "27 (на 08.09.2026)")

    def test_extracts_first_person_profession(self):
        facts = extract_profile_facts(
            "Привіт! Я графічний дизайнер і живу в Одесі.",
            self.date,
        )
        self.assertEqual(facts[0].fact_type, "profession")
        self.assertIn("дизайнер", facts[0].value)

    def test_does_not_treat_discussed_profession_as_personal(self):
        facts = extract_profile_facts(
            "Шукаємо графічного дизайнера в команду",
            self.date,
        )
        self.assertEqual(facts, [])

    def test_extracts_personal_portfolio_link(self):
        facts = extract_profile_facts(
            "Ось моє портфоліо: https://example.com/me",
            self.date,
        )
        self.assertEqual(facts[0].fact_type, "portfolio")

    def test_ignores_unattributed_link(self):
        facts = extract_profile_facts(
            "Корисне портфоліо: https://example.com/other",
            self.date,
        )
        self.assertEqual(facts, [])
