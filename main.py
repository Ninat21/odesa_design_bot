import asyncio

from aiogram import Dispatcher

from bot import bot


async def main():
    dp = Dispatcher()

    print("Бот запущено 🚀")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())