from app.database.repositories.statistics import StatisticsRepository


class StatisticsService:
    def __init__(
        self,
        statistics: StatisticsRepository,
    ):
        self.statistics = statistics

    async def totals(self) -> tuple[int, int]:
        return await self.statistics.get_totals()

    async def members(self):
        return await self.statistics.get_current_members()

    async def top10(self):
        return await self.statistics.get_top_users(
            limit=10,
        )

    async def top20(self):
        return await self.statistics.get_top_users(
            limit=20,
        )

    async def top10_90(self):
        return await self.statistics.get_top_users(
            limit=10,
            days=90,
        )

    async def top20_90(self):
        return await self.statistics.get_top_users(
            limit=20,
            days=90,
        )

    async def users_without_messages(self):
        return await self.statistics.get_users_without_messages()

    async def users_with_one_message(self):
        return await self.statistics.get_users_with_one_message()

    async def inactive30(self):
        return await self.statistics.get_inactive_users(
            days=30,
        )

    async def inactive90(self):
        return await self.statistics.get_inactive_users(
            days=90,
        )

    async def inactive3m(self):
        return await self.statistics.get_inactive_members(
            days=90,
        )

    async def oldest20(self):
        return await self.statistics.get_oldest_members(
            limit=20,
        )

    async def oldest50(self):
        return await self.statistics.get_oldest_members(
            limit=50,
        )

    async def new30(self):
        return await self.statistics.get_new_members(
            days=30,
        )
