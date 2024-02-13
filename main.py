import discord
from discord.ext import commands 
intents = discord.Intents.default() 
intents.message_content = True 
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('MTIwNTMxNzUyMDQwNDUyMTAyMA.GqUNF3.M43r5FiH7-VW53wc_h3UHCfPbanxTPBdNAZ3w8')
