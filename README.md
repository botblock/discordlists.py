[![PyPI](https://img.shields.io/pypi/v/discordlists.py.svg)](https://pypi.org/project/discordlists.py/)

# discordlists.py
**A simple API wrapper for botblock.org providing server count posting to all bot lists and fetching bot information from all.**

## Installation

Install via pip (recommended)

    pip install discordlists.py

## Features

* POST server count
* AUTOMATIC server count updating
* ALL bot lists' APIs included
* GET bot information from all bot lists and Discord

## Example Discord.py Cog for Posting Server Count

```Python
from discord.ext import commands

import discordlists

with open('config.txt') as f:
    config = [g.strip('\r\n ') for g in f.readlines()]


class DiscordListsPost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = discordlists.Client(self.bot)  # Create a Client instance
        self.api.set_auth(config[1], config[2])  # Set authorisation token for a bot list
        self.api.start_loop()  # Posts the server count automatically every 30 minutes

    @commands.command()
    async def post(self, ctx: commands.Context):
        """
        Manually posts guild count using discordlists.py (BotBlock)
        """
        try:
            result = await self.api.post_count()
        except Exception as e:
            await ctx.send("Request failed: `{}`".format(e))
            return

        await ctx.send("Successfully manually posted server count ({:,}) to {:,} lists."
                       "\nFailed to post server count to {:,} lists.".format(self.api.server_count,
                                                                             len(result["success"].keys()),
                                                                             len(result["failure"].keys())))


def setup(bot):
    bot.add_cog(DiscordListsPost(bot))

```

## Example Discord.py Cog for Getting Bot Info

```Python
from discord.ext import commands

import discordlists


class DiscordListsGet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = discordlists.Client(self.bot)  # Create a Client instance

    @commands.command()
    async def get(self, ctx: commands.Context, bot_id: int = None):
        """
        Gets a bot using discordlists.py (BotBlock)
        """
        if bot_id is None:
            bot_id = self.bot.user.id
        try:
            result = (await self.api.get_bot_info(bot_id))[1]
        except Exception as e:
            await ctx.send("Request failed: `{}`".format(e))
            return

        await ctx.send("Bot: {}#{} ({})\nOwners: {}\nServer Count: {}".format(
            result['username'], result['discriminator'], result['id'],
            ", ".join(result['owners']) if result['owners'] else "Unknown",
            "{:,}".format(result['server_count']) if result['server_count'] else "Unknown"
        ))


def setup(bot):
    bot.add_cog(DiscordListsGet(bot))

```

## Discussion, Support and Issues
For general support and discussion of this project, please join the Discord server: https://discord.gg/qyXqA7y \
[![Discord Server](https://discordapp.com/api/guilds/204663881799303168/widget.png?style=banner2)](https://discord.gg/qyXqA7y)

To check known bugs and see planned changes and features for this project, please see the GitHub issues.\
Found a bug we don't already have an issue for? Please report it in a new GitHub issue with as much detail as you can!
