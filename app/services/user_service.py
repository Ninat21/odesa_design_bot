from app.database.repositories.users import UserRepository


class UserService:
    def __init__(
        self,
        users: UserRepository,
    ):
        self.users = users

    async def get_or_create_user(
        self,
        telegram_id: int,
        **data,
    ):
        user = await self.users.get_by_telegram_id(
            telegram_id
        )

        if user:
            return user

        return await self.users.create(
            telegram_id=telegram_id,
            **data,
        )

    async def get_by_telegram_id(self, telegram_id: int):
        return await self.users.get_by_telegram_id(telegram_id)

    async def get_by_id(self, user_id: int):
        return await self.users.get_by_id(user_id)

    async def get_by_username(self, username: str):
        return await self.users.get_by_username(username)

    async def save(self, user):
        return await self.users.save(user)

    async def delete(self, user):
        await self.users.delete(user)
