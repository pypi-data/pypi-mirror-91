from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import discord


@dataclass
class Like:
    bot_id: int
    author_id: int
    date: datetime
    _bot: discord.Client

    @classmethod
    def from_data(cls, data: dict, bot: discord.Client):
        try:
            date = datetime.fromtimestamp(data["date"] / 1000)
        except OSError:
            date = datetime.max

        like = {
            "bot_id": int(data["bot_id"]),
            "author_id": int(data["author_id"]),
            "date": date
        }

        return cls(**like, _bot=bot)

    @property
    def author(self) -> Optional[discord.User]:
        return self._bot.get_user(self.author_id)


@dataclass
class Comment:
    id: str
    bot_id: int
    author_id: int
    content: str
    date: datetime
    _bot: discord.Client

    @classmethod
    def from_data(cls, data: dict, bot: discord.Client):
        try:
            date = datetime.fromtimestamp(data["commented"] / 1000)
        except OSError:
            date = datetime.max

        comment = {
            "id": data["comment_id"],
            "bot_id": int(data["bot_id"]),
            "author_id": int(data["author_id"]),
            "content": data["content"],
            "date": date
        }

        return cls(**comment, _bot=bot)

    @property
    def author(self) -> Optional[discord.User]:
        return self._bot.get_user(self.author_id)


@dataclass
class Stats:
    bot_id: int
    guild_count: int
    channel_count: int
    user_count: int
    date: datetime
    _bot: discord.Client

    @classmethod
    def from_data(cls, data: dict, bot: discord.Client):
        try:
            date = datetime.fromtimestamp(data["date"] / 1000)
        except OSError:
            date = datetime.max

        stats = {
            "bot_id": int(data["bot_id"]),
            "guild_count": data["guilds"],
            "channel_count": data["channels"],
            "user_count": data["users"],
            "date": date
        }

        return cls(**stats, _bot=bot)
