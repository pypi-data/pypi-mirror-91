# DiscordBotsList.py

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7b97ef7307d44f7285935ee1c6f336aa)](https://app.codacy.com/gh/MrSpinne/DiscordBotsList.py?utm_source=github.com&utm_medium=referral&utm_content=MrSpinne/DiscordBotsList.py&utm_campaign=Badge_Grade_Settings)

An API wrapper for discordbotslist.us.to written in Python

## Installation
Install via pip

    pip install dbl-us-to

## Features
  - GET bot likes and check if user has liked
  - GET bot comments
  - GET bot stats
  - POST your own bot stats

## Methods
In the following I'll be explaining all methods this library offers.
Notice that you have to await these since they are async.

### DBLClient.get_likes(bot_id)
**Arguments**

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| bot_id    | int  | The bot id to get the likes of. Defaults to your own bot id.

**Returns**
List of `Like` objects. These have the following attributes.

| Attributes | Type            | Description |
| ---------- | --------------- | ----------- |
| bot_id     | int             | The bot id the like is associated with
| author     | discord.User    | User object if cached else `None`. Use `author_id` as fallback.
| author_id  | int             | The id of the author who liked
| date       | datetime.datime | When the like was created

### DBLClient.get_comments(bot_id)
**Arguments**

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| bot_id    | int  | The bot id to get the comments of. Defaults to your own bot id.

**Returns**
List of `Comment` objects. These have the following attributes.

| Attributes | Type            | Description |
| ---------- | --------------- | ----------- |
| id         | str             | Unique id of the comment
| bot_id     | int             | The bot id the comment is associated with
| author     | discord.User    | User object if cached else `None`. Use `author_id` as fallback.
| author_id  | int             | The id of the author who liked
| content    | str             | The content of the comment
| date       | datetime.datime | When the comment was created

### DBLClient.get_stats(bot_id)
**Arguments**

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| bot_id    | int  | The bot id to get the stats of. Defaults to your own bot id.

**Returns**
`Stats` object. These have the following attributes.

| Attributes  | Type            | Description |
| ----------- | --------------- | ----------- |
| bot_id      | int             | The bot id the stats are associated with
| guild_count | int             | The amount of guilds the bot is on
| channel_count | int             | The amount of all guild channels the bot can see
| user_count | int             | The amount of all users the bot can see
| date        | datetime.datime | When the stats was last updated

## DBLClient.post_stats()
Updates your bots stats on DiscordBotsList.us.to

## Example

```python
import discord
from dbl_us_to import DBLClient


intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents=intents)

api_key = "DiscordBotsList API Key"
dbl = DBLClient(bot, api_key)


@bot.event
async def on_ready():
    likes = dbl.get_likes()
    for like in likes:
        print(like.author)
        

bot.run("bot token")
```