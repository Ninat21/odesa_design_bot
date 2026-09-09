from app.database.repositories.profiles import ProfileRepository


class ProfileService:
    def __init__(
        self,
        profiles: ProfileRepository,
        profile_facts=None,
    ):
        self.profiles = profiles
        self.profile_facts = profile_facts

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

    async def get_card(self, user_id: int):
        profile = await self.profiles.get_by_user_id(user_id)
        facts = await self.profile_facts.list_with_sources(user_id)
        return profile, facts

    async def get_fact(self, fact_id: int):
        return await self.profile_facts.get_by_id(fact_id)

    async def verify_fact(self, fact):
        return await self.profile_facts.verify(fact)

    async def update_fact_value(self, fact, value: str):
        return await self.profile_facts.update_value(fact, value)

    async def delete_fact(self, fact) -> None:
        await self.profile_facts.delete(fact)
