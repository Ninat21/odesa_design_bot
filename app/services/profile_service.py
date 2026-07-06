from app.database.repositories.profiles import ProfileRepository


class ProfileService:
    def __init__(
        self,
        profiles: ProfileRepository,
    ):
        self.profiles = profiles

    async def get_by_user_id(
        self,
        user_id: int,
    ):
        return await self.profiles.get_by_user_id(user_id)

    async def create(
        self,
        **data,
    ):
        return await self.profiles.create(**data)

    async def save(
        self,
        profile,
    ):
        return await self.profiles.save(profile)

    async def delete(
        self,
        profile,
    ):
        await self.profiles.delete(profile)