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
        <img src="https://img.shields.io/pypi/v/discordlists.py.svg?style=flat-square" alt="PyPi Version">
    </a>
    <a href="http://slack.mattcowley.co.uk/" target="_blank">
        <img src="https://img.shields.io/badge/slack-MattIPv4-blue.svg?style=flat-square" alt="Slack">
    </a>
</p>

----

<!-- Content -->
## Installation

Install via pip (recommended)

    pip install discordlists.py

## Features

* POST server count
* AUTOMATIC server count updating
* ALL bot lists' APIs included
* GET bot information from all bot lists and Discord

## Example Discord.py Rewrite cog


```Python
import discordlists

from discord.ext import commands
from discord.ext.commands import Context


class DiscordLists:
    def __init__(self, bot):
        self.bot = bot
        self.api = discordlists.Client(self.bot)  # Create a Client instance
        self.api.set_auth("botsfordiscord.com", "cfd28b742fd7ddfab1a211934c88f3d483431e639f6564193") # Set authorisation token for a bot list
        self.api.start_loop()  # Posts the server count automatically every 30 minutes

    @commands.command()
    async def get_bot(self, ctx: Context, bot_id: int):
        """
        Gets a bot using discordlists.py
        """
        try:
            result = await self.api.get_bot_info(bot_id)
        except:
            await ctx.send("Request failed")
            return
        
        await ctx.send("Bot: {}#{} ({})\nOwners: {}\nServer Count: {:,}".format(
            result['username'], result['discriminator'], result['id'], 
            ", ".join(result['owners']), result['server_count']
        ))

def setup(bot):
    bot.add_cog(DiscordLists(bot))
```

<!-- Contributing -->
## Contributing

Contributions are always welcome to this project!\
Take a look at any existing issues on this repository for starting places to help contribute towards, or simply create your own new contribution to the project.

Please make sure to follow the existing standards within the project such as code styles, naming conventions and commenting/documentation.

When you are ready, simply create a pull request for your contribution and I will review it whenever I can!

Need to chat about the project and how you can get involved?\
Join the Slack workspace to find the appropriate channel, talk to other contributors and myself: [slack.mattcowley.co.uk](http://slack.mattcowley.co.uk)

<!-- Discussion & Support -->
## Discussion, Support and Issues

Need support with this project or have found an issue?
> Please check the project's issues page first!

Not found what you need?
* Create a GitHub issue here to report the situation, as much detail as you can!
* _or,_ You can join our Slack workspace to discuss the issue or to get support for the project:
<a href="http://slack.mattcowley.co.uk/" target="_blank">
    <img src="https://img.shields.io/badge/slack-MattIPv4-blue.svg?logo=slack&logoWidth=30&logoColor=blue&style=popout-square" alt="Slack" height="60">
</a>
