from typing import Any, Callable, Dict

from aiogram import BaseMiddleware

from app.core.logger import logger


class ErrorMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable,
        event: Any,
        data: Dict[str, Any],
    ):

        try:
            return await handler(event, data)

        except Exception:

            logger.exception("Помилка під час обробки оновлення")

            raise
