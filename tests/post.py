import json

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

        await ctx.send("```json\n{}\n```".format(json.dumps(result)[:1980]))
        await ctx.send("Successfully manually posted server count ({:,}) to {:,} lists."
                       "\nFailed to post server count to {:,} lists.".format(self.api.server_count,
                                                                             len(result["success"].keys()),
                                                                             len(result["failure"].keys())))


def setup(bot):
    bot.add_cog(DiscordListsPost(bot))
