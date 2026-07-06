from aiogram.types import User as AiogramUser
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

    async def execute_telethon(
        self,
        telegram_user: TelethonUser,
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

        user = await self.users.get_by_telegram_id(
            telegram_id,
        )

        if user is None:

            return await self.users.create(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_bot=is_bot,
                language_code=language_code,
                is_premium=is_premium,
            )

        changed = False

        if user.username != username:
            user.username = username
            changed = True

        if user.first_name != first_name:
            user.first_name = first_name
            changed = True

        if user.last_name != last_name:
            user.last_name = last_name
            changed = True

        if user.language_code != language_code:
            user.language_code = language_code
            changed = True

        if user.is_premium != is_premium:
            user.is_premium = is_premium
            changed = True

        if user.is_bot != is_bot:
            user.is_bot = is_bot
            changed = True

        if changed:
            await self.users.save(user)

        return user