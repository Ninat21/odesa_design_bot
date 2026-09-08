import asyncio

from aiogram import Dispatcher

from app.bot import bot
from app.core.logger import logger

# from app.handlers.welcome_new import router as welcome_new_router
from app.handlers.admin.statistics import router as statistics_router
from app.handlers.ping import router as ping_router
from app.handlers.setup import router as setup_router
from app.handlers.stats import router as stats_router
from app.handlers.welcome import router as welcome_router
from app.health import start_health_server
from app.middlewares.database import DatabaseMiddleware
from app.middlewares.error import ErrorMiddleware
from app.middlewares.message_persistence import MessagePersistenceMiddleware


def configure_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware(ErrorMiddleware())

    # Message persistence must run in the outer scope. Inner middleware is only
    # called after a handler filter matches, while most community messages do
    # not have a dedicated handler.
    dp.message.outer_middleware(DatabaseMiddleware())
    dp.message.outer_middleware(MessagePersistenceMiddleware())
    dp.edited_message.outer_middleware(DatabaseMiddleware())
    dp.edited_message.outer_middleware(MessagePersistenceMiddleware())

    dp.chat_member.middleware(DatabaseMiddleware())


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    configure_middlewares(dp)

    dp.include_router(welcome_router)
    dp.include_router(setup_router)
    dp.include_router(ping_router)
    dp.include_router(stats_router)
    dp.include_router(statistics_router)
    # dp.include_router(welcome_new_router)

    return dp


async def main():
    dp = create_dispatcher()
    health_runner = await start_health_server()

    try:
        logger.info("Бот запущений")
        await bot.delete_webhook(drop_pending_updates=False)
        await dp.start_polling(bot)
    finally:
        await health_runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
