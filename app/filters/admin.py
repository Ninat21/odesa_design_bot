from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.config import Config


class AdminFilter(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in Config.ADMIN_IDS