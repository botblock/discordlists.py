from discord.ext import commands

with open('config.txt') as f:
    config = [g.strip('\r\n ') for g in f.readlines()]

bot = commands.Bot('!')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.load_extension('post')
bot.load_extension('get')
bot.run(config[0])
