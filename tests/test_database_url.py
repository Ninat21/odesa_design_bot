import unittest

from app.database.database import normalize_database_url


class NormalizeDatabaseUrlTests(unittest.TestCase):
    def test_converts_postgresql_url_to_asyncpg(self) -> None:
        url = "postgresql://user:password@host:5432/database?sslmode=require"

        self.assertEqual(
            normalize_database_url(url),
            "postgresql+asyncpg://user:password@host:5432/database?ssl=require",
        )

    def test_keeps_existing_asyncpg_driver(self) -> None:
        url = "postgresql+asyncpg://user:password@host:5432/database"

        self.assertEqual(normalize_database_url(url), url)


if __name__ == "__main__":
    unittest.main()
