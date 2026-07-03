import asyncio

from aiogram import Dispatcher

from app.bot import bot

from app.handlers.welcome import router as welcome_router
from app.handlers.setup import router as setup_router

import asyncio
import traceback

from aiogram import Dispatcher

from app.bot import bot

from app.handlers.welcome import router as welcome_router
from app.handlers.setup import router as setup_router


async def main():
    try:
        dp = Dispatcher()

        dp.include_router(welcome_router)
        dp.include_router(setup_router)

        print("Бот запущено 🚀")

        await dp.start_polling(bot)

    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
async def main():
    dp = Dispatcher()

    dp.include_router(welcome_router)

    dp.include_router(setup_router)

    print("Бот запущено 🚀")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

    