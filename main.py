import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
#loading env file

load_dotenv() 

#retriving the token
DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
print(type(DISCORD_API_TOKEN))


def run(): 
    intents = discord.Intents.default() 
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(bot.user)
        print(bot.user.id)
        print("--------------------------")
        
        
    @bot.command
    async def say(ctx, what): 
        await ctx.send(what)
    
    
    # if (len(message.attachments) != 0): 
    @bot.event 
    async def on_message(message):
        if message.author == bot.user:
            return
        
       
        listSniped = message.mentions
        for i in listSniped:
            print(i)
        print(listSniped)
        sniper_id = message.author.id
        sender = message.author.display_name
        await message.channel.send(f"{sender} is the GOAT")
        
        
        
        
        
        
    bot.run(DISCORD_API_TOKEN) #remove this and ENV it later 


if __name__ == "__main__":
    run() 