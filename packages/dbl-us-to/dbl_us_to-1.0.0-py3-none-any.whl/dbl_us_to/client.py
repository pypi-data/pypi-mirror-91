import logging
from typing import List

import discord

from .http import HTTPClient
from .model import Like, Comment, Stats

logger = logging.getLogger(__name__)


class DBLClient:
    def __init__(self, bot: discord.Client, api_key: str):
        self._bot = bot
        self._http = HTTPClient(api_key, self._bot.loop)

    async def get_likes(self, bot_id: int = None) -> List[Like]:
        bot_id = bot_id or self._bot.user.id
        likes = await self._http.get_likes(bot_id)
        return [Like.from_data(data, self._bot) for data in likes]

    async def get_comments(self, bot_id: int = None) -> List[Comment]:
        bot_id = bot_id or self._bot.user.id
        comments = await self._http.get_comments(bot_id)
        return [Comment.from_data(data, self._bot) for data in comments]

    async def get_stats(self, bot_id: int = None) -> Stats:
        bot_id = bot_id or self._bot.user.id
        data = await self._http.get_stats(bot_id)
        return Stats.from_data(data, self._bot)

    async def post_stats(self):
        await self._http.post_stats(
            len(self._bot.guilds),
            len(list(self._bot.get_all_channels())),
            len(self._bot.users),
            self._bot.user.id
        )
