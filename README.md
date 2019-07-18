<!-- Source: https://github.com/MattIPv4/template/blob/master/README.md -->

<!-- Title -->
<h1 align="center" id="discordlistspy">
    discordlists.py
</h1>

<!-- Tag line -->
<h3 align="center">A simple API wrapper for botblock.org providing server count posting to all bot lists and fetching bot information from all.</h3>

<!-- Badges -->
<p align="center">
    <a href="https://pypi.org/project/discordlists.py/" target="_blank">
        <img src="https://img.shields.io/pypi/v/discordlists.py.svg?style=flat-square" alt="PyPi Version"/>
    </a>
    <a href="http://patreon.mattcowley.co.uk/" target="_blank">
        <img src="https://img.shields.io/badge/patreon-IPv4-blue.svg?style=flat-square" alt="Patreon"/>
    </a>
    <a href="http://slack.mattcowley.co.uk/" target="_blank">
        <img src="https://img.shields.io/badge/slack-MattIPv4-blue.svg?style=flat-square" alt="Slack"/>
    </a>
</p>

----

<!-- Content -->
## Installation

Install via pip (recommended)

```Shell
python3 -m pip install discordlists.py
```

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

<!-- Contributing -->
## Contributing

Contributions are always welcome to this project!\
Take a look at any existing issues on this repository for starting places to help contribute towards, or simply create your own new contribution to the project.

Please make sure to follow the existing standards within the project such as code styles, naming conventions and commenting/documentation.

When you are ready, simply create a pull request for your contribution and I will review it whenever I can!

### Donating

You can also help me and the project out by contributing through a donation on PayPal or by supporting me monthly on my Patreon page.
<p>
    <a href="http://patreon.mattcowley.co.uk/" target="_blank">
        <img src="https://img.shields.io/badge/patreon-IPv4-blue.svg?logo=patreon&logoWidth=30&logoColor=F96854&style=popout-square" alt="Patreon"/>
    </a>
    <a href="http://paypal.mattcowley.co.uk/" target="_blank">
        <img src="https://img.shields.io/badge/paypal-Matt%20(IPv4)%20Cowley-blue.svg?logo=paypal&logoWidth=30&logoColor=00457C&style=popout-square" alt="PayPal"/>
    </a>
</p>

<!-- Discussion & Support -->
## Discussion, Support and Issues

Need support with this project, have found an issue or want to chat with others about contributing to the project?
> Please check the project's issues page first for support & bugs!

Not found what you need here?
* If you have an issue, please create a GitHub issue here to report the situation, include as much detail as you can!
* _or,_ You can join our Slack workspace to discuss any issue, to get support for the project or to chat with contributors and myself:

<a href="http://slack.mattcowley.co.uk/" target="_blank">
    <img src="https://img.shields.io/badge/slack-MattIPv4-blue.svg?logo=slack&logoWidth=30&logoColor=blue&style=popout-square" alt="Slack" height="60">
</a>
