from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.database.database import SessionLocal
from app.database.uow import UnitOfWork
from app.services.factory import ServiceFactory


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[
            [TelegramObject, dict[str, Any]],
            Awaitable[Any],
        ],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:

        async with SessionLocal() as session:

            data["session"] = session

            uow = UnitOfWork(session)
            services = ServiceFactory(uow)

            data["uow"] = uow
            data["services"] = services

            try:
                result = await handler(event, data)

                await session.commit()

                return result

            except Exception:

                await session.rollback()

                raise