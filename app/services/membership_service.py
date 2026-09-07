from datetime import datetime

from aiogram.types import User as TelegramUser

from app.database.models import User
from app.database.repositories.users import UserRepository
from app.services.message_processor.steps.save_user import SaveUserStep


class MembershipService:
    def __init__(self, users: UserRepository):
        self.users = users
        self.save_user = SaveUserStep(users)

    async def join(self, telegram_user: TelegramUser, joined_at: datetime) -> User:
        user = await self.save_user.execute(telegram_user)
        return await self.users.mark_joined(user, joined_at)

    async def leave(self, telegram_user: TelegramUser, left_at: datetime) -> User:
        user = await self.save_user.execute(telegram_user)
        return await self.users.mark_left(user, left_at)
