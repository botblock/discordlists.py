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
