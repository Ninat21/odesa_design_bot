import asyncio

from aiogram import Dispatcher

from app.bot import bot
from app.handlers.welcome import router as welcome_router
from app.handlers.setup import router as setup_router
from app.handlers.ping import router as ping_router

from app.middlewares.database import DatabaseMiddleware
from app.handlers.stats import router as stats_router
from app.database import create_database
from app.middlewares.database import DatabaseMiddleware


async def main():
    dp = Dispatcher()
    

    dp.message.middleware(DatabaseMiddleware())
    create_database()

    dp.include_router(welcome_router)
    dp.include_router(setup_router)
    dp.include_router(ping_router)
    dp.include_router(stats_router)

    print("Бот запущено 🚀")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())