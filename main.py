import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
import sqlite3
#loading env file

load_dotenv() 

#retriving the token
DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
print(type(DISCORD_API_TOKEN))


#database connections 

sqliteConnection = sqlite3.connect('SniperBot.db')
print ("Opened database successfully")

cursor = sqliteConnection.cursor()

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
    
        
        if (len(message.attachments) != 0):
            listSniped = message.mentions
            listIDsniped = [ x.id for x in listSniped]
            sniper_id = message.author.id
            sniper = message.author.display_name
            sniped_names = ", ".join([member.display_name for member in listSniped])
            sniper_count = 0
            
            userHere = sqliteConnection.execute(f'''SELECT EXISTS(SELECT 1 FROM SNIPERBOT WHERE ID = "{sniper_id}");''')
            userHereList = [ x for x in userHere]
            userHerefinal = userHereList[0][0]
        
            
            if not userHerefinal:
                await message.channel.send(f"{sniper} is not registered!. Please register by using !register command")
                return 
            
            if len(listSniped) == 0:
                await message.channel.send(f"Can't snipe without tagging the people")
                return
            
            sqliteConnection.execute(f"UPDATE SNIPERBOT SET SNIPES = SNIPES + 1 WHERE ID = {sniper_id}")
            sqliteConnection.execute(f"UPDATE SNIPERBOT SET SNIPPED = SNIPPED + 1 WHERE ID IN ({', '.join(map(str, listIDsniped))})")
            sqliteConnection.commit()
            sniper_count = sqliteConnection.execute(f"SELECT SNIPES FROM SNIPERBOT WHERE ID = {sniper_id}")
            result = sniper_count
            print("result for sniper count from graph: ", result)
            sniper_count_value = 0 #result[0]  # Assuming SNIPES is the second column in the SELECT query
            await message.channel.send(f"{sniper} sniped {sniped_names}. {sniper} has snipped {sniper_count_value} times!!")
        else:
            await message.channel.send(f"Can't snipe without a photo lols")
            return
            
        
        
        
        
        
    bot.run(DISCORD_API_TOKEN) #remove this and ENV it later 


if __name__ == "__main__":
    run() 