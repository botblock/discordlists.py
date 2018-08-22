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
* GET bot information from all bot lists

## Example Discord.py Rewrite cog


```Python
    import discordlists


    class Stats:
        def __init__(self, bot):
            self.bot = bot
            self.api = discordlists.Client(self.bot)  # Create a Client instance
            self.api.set_auth("botsfordiscord.com", "cfd28b742fd7ddfab1a211934c88f3d483431e639f6564193") # Set authorisation token for a bot list
            self.api.start_loop()  # Posts the server count automatically every 30 minutes

    def setup(bot):
        bot.add_cog(Stats(bot))
```

## Discussion, Support and Issues
For general support and discussion of this project, please join the Discord server: https://discord.gg/qyXqA7y \
[![Discord Server](https://discordapp.com/api/guilds/204663881799303168/widget.png?style=banner2)](https://discord.gg/qyXqA7y)

To check known bugs and see planned changes and features for this project, please see the GitHub issues.\
Found a bug we don't already have an issue for? Please report it in a new GitHub issue with as much detail as you can!