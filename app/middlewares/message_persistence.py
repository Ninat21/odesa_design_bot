from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.config import Config
from app.services.factory import ServiceFactory


class MessagePersistenceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        if event.chat.id == Config.GROUP_ID and event.from_user is not None:
            services: ServiceFactory = data["services"]
            await services.message_processor.process(
                telegram_user=event.from_user,
                telegram_message=event,
            )
            await data["session"].commit()

        return await handler(event, data)
