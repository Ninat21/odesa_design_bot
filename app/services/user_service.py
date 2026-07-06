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

    async def save(self, user):
        return await self.users.save(user)

    async def delete(self, user):
        await self.users.delete(user)