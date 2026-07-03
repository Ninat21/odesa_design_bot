from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.database.crud import add_message_from_aiogram, add_user


class DatabaseMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:

        if isinstance(event, Message):

            if event.from_user:

                add_user(
                    telegram_id=event.from_user.id,
                    username=event.from_user.username,
                    first_name=event.from_user.first_name,
                    last_name=event.from_user.last_name,
                )

                add_message_from_aiogram(event)

        return await handler(event, data)