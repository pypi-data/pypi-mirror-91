import logging
from asyncio import AbstractEventLoop

import aiohttp

logger = logging.getLogger(__name__)


class HTTPClient:
    def __init__(self, api_key: str, loop: AbstractEventLoop):
        self.base = "https://discordbotslist.us.to/api"
        self.api_key = api_key
        self.loop = loop
        self.session = aiohttp.ClientSession(loop=loop, raise_for_status=True)

    async def request(self, method: str, endpoint: str, data: dict = None) -> dict:
        url = self.base + endpoint

        async with self.session.request(method, url, json=data) as resp:
            data = await resp.json()
            logger.debug(f"{resp.method} {resp.url} returned {data}")
            return data

    async def get_likes(self, bot_id: int) -> list:
        data = await self.request("GET", f"/bot/likes/{bot_id}")
        return data["likes"]

    async def get_comments(self, bot_id: int) -> list:
        data = await self.request("GET", f"/bot/comments/{bot_id}")
        return data["comments"]

    async def get_stats(self, bot_id: int) -> dict:
        data = await self.request("GET", f"/bot/stats/{bot_id}")
        return data["stats"]

    async def post_stats(self, guild_count: int, channel_count: int, user_count: int, bot_id: int):
        payload = {
            "api_key": self.api_key,
            "guilds": guild_count,
            "channels": channel_count,
            "users": user_count
        }
        return await self.request("POST", f"/bot/stats/{bot_id}", payload)
