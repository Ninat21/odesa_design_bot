import argparse
import asyncio
import os

from aiogram import Bot
from dotenv import load_dotenv

from app.services.member_sync import synchronize_known_members


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synchronize known users with Telegram chat membership."
    )
    parser.add_argument(
        "chat_id",
        nargs="?",
        type=int,
        default=os.getenv("GROUP_ID"),
    )
    args = parser.parse_args()
    if args.chat_id is None:
        parser.error("chat_id argument or GROUP_ID is required")
    return args


async def main() -> None:
    load_dotenv()
    args = parse_args()
    bot = Bot(os.environ["BOT_TOKEN"])
    try:
        result = await synchronize_known_members(
            bot,
            args.chat_id,
        )
        print("Known Telegram users synchronized:", result)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
