import json

import discord

import discordlists

with open('config.txt') as f:
    config = [g.strip('\r\n ') for g in f.readlines()]

bot_client = discord.Client()
api_client = discordlists.Client(bot_client)

# POST Test: Setup BFD API auth token
api_client.set_auth("botsfordiscord.com", config[1])


@bot_client.event
async def on_ready():
    print('Logged in as')
    print(bot_client.user.name)
    print(bot_client.user.id)
    print('------')


@bot_client.event
async def on_message(message):
    # POST Test: Send guild count through client using d.py bot instance and return result
    if message.content.startswith('!post'):
        result = await api_client.post_count()
        result = json.dumps(result)[:2000]
        await bot_client.send_message(message.channel, result)


bot_client.run(config[0])
