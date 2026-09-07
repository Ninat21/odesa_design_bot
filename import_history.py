import argparse
import asyncio

from app.services.importer import import_telegram_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import a Telegram JSON export.")
    parser.add_argument(
        "path",
        nargs="?",
        default="result.json",
        help="Path to the Telegram result.json export.",
    )
    return parser.parse_args()


async def main():
    result = await import_telegram_json(parse_args().path)

    print()
    print("========== ГОТОВО ==========")
    print(f"👥 Користувачів: {result['users']}")
    print(f"💬 Повідомлень: {result['messages']}")
    print("============================")


if __name__ == "__main__":
    asyncio.run(main())
