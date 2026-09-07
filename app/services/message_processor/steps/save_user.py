from datetime import datetime
from typing import TYPE_CHECKING

from aiogram.types import User as AiogramUser

if TYPE_CHECKING:
    from telethon.tl.types import User as TelethonUser

from app.database.models import User
from app.database.repositories.users import UserRepository


class SaveUserStep:
    def __init__(
        self,
        users: UserRepository,
    ):
        self.users = users

    async def execute(
        self,
        telegram_user: AiogramUser,
    ) -> User:

        return await self._save_user(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            is_bot=telegram_user.is_bot,
            language_code=telegram_user.language_code,
            is_premium=getattr(
                telegram_user,
                "is_premium",
                False,
            ),
        )

    async def execute_member(
        self,
        telegram_user: AiogramUser,
        observed_at: datetime,
    ) -> User:
        user = await self.execute(telegram_user)
        return await self.users.mark_present(user, observed_at)

    async def execute_telethon(
        self,
        telegram_user: "TelethonUser",
    ) -> User:

        return await self._save_user(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            is_bot=telegram_user.bot,
            language_code=None,
            is_premium=getattr(
                telegram_user,
                "premium",
                False,
            ),
        )

    async def _save_user(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str | None,
        last_name: str | None,
        is_bot: bool,
        language_code: str | None,
        is_premium: bool,
    ) -> User:
        return await self.users.upsert_by_telegram_id(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_bot=is_bot,
            language_code=language_code,
            is_premium=is_premium,
        )
