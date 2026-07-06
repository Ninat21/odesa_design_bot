import asyncio

from aiogram import Dispatcher

from app.bot import bot
from app.core.logger import logger
from app.handlers.ping import router as ping_router
from app.handlers.setup import router as setup_router
from app.handlers.stats import router as stats_router
from app.handlers.welcome import router as welcome_router
from app.middlewares.database import DatabaseMiddleware
from app.middlewares.error import ErrorMiddleware
# from app.handlers.welcome_new import router as welcome_new_router

async def main():
    dp = Dispatcher()

    # Middleware
    dp.update.middleware(ErrorMiddleware())
    dp.message.middleware(DatabaseMiddleware())

    # Routers
    dp.include_router(welcome_router)
    dp.include_router(setup_router)
    dp.include_router(ping_router)
    dp.include_router(stats_router)
   # dp.include_router(welcome_new_router)

    logger.info("Бот запущений")
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
