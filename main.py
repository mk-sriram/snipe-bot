import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
import sqlite3
#loading env file

load_dotenv() 

#retriving the token
DISCORD_API_TOKEN = os.getenv('DISCORD_API_TOKEN')
#database connections 

sqliteConnection = sqlite3.connect('SniperBot.db')
print ("Opened database successfully")

cursor = sqliteConnection.cursor()

def run(): 
    intents = discord.Intents.default() 
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
        
    @bot.event
    async def on_ready():
        print(bot.user)
        print(bot.user.id)
        print("--------------------------")
        
    
    
    # if (len(message.attachments) != 0): 
    @bot.event 
    async def on_message(message):
        if message.author == bot.user:
            return
        if (message.content.startswith("!leader")):
            rows = sqliteConnection.execute(f'''SELECT * FROM SNIPERBOT ORDER BY SNIPES DESC''')
            embed=discord.Embed(title="Leaderboard", color=discord.Color.green())
            embed.add_field(name="Name", value="", inline=True)
            embed.add_field(name="Snipes" , value="", inline=True)
            embed.add_field(name="Sniped", value="", inline=True)
            for row in rows:
                #print(row)
               
                userName = await bot.fetch_user(row[0])
                embed.add_field(name="", value= userName, inline=True)
                embed.add_field(name="", value=row[1], inline=True)
                embed.add_field(name="", value=row[2], inline=True)
            await message.channel.send(embed=embed)
            return
            
        if (message.content.startswith("!score")):
            authorID = message.author.id
            author = message.author.display_name
            rows = sqliteConnection.execute(f'''SELECT * FROM SNIPERBOT WHERE ID= "{authorID}"''')
            for row in rows:
                await message.channel.send(f"{author} has `{row[1]}` snipes and has been sniped `{row[2]}` times")
            return
        
        if(message.content.startswith("!help")):
           embed1=discord.Embed(title="Instructions", color=discord.Color.orange())
           embed1.description = "1.Tag @user along with picture in the same message\n2.`!score` shows your score\n3.`!leader` shows the leaderboard\n4.`!help` for instructions"
           await message.channel.send(embed=embed1)
           return
            
        if (len(message.mentions) != 0):
            if (len(message.attachments) != 0):
               
                
                listSniped = message.mentions
                listIDsniped = [ x.id for x in listSniped]
                 
                lastMessage = message.channel.last_message
                lastSniperID = lastMessage.author.id 
                
                if lastSniperID in listIDsniped:
                    #check rn doesnt do anything as the previous msg is always from the SNipe bot and not the user 
                    await message.channel.send(f"Can't snipe the sniper")
                    return 
                listNamesSniped = [ await bot.fetch_user(x) for x in listIDsniped]
                print(listNamesSniped)
                
                sniper_id = message.author.id
                sniper = message.author.display_name
                sniped_names = ", ".join([member.display_name for member in listSniped])
                sniper_count = 0
                
                userHere = sqliteConnection.execute(f'''SELECT EXISTS(SELECT 1 FROM SNIPERBOT WHERE ID = "{sniper_id}");''')
                userHereList = [ x for x in userHere]
                userHerefinal = userHereList[0][0]
            
                
                if not userHerefinal:
                    data_to_insert = [(sniper_id, 0, 0)]
                    sql_query = "INSERT INTO SNIPERBOT (ID, SNIPES, SNIPPED) VALUES (?, ?, ?)"
                    cursor.executemany(sql_query, data_to_insert)
                    print("user was registered")

                    
                
                if len(listSniped) == 0:
                    await message.channel.send(f"Can't snipe without tagging the people")
                    return
                
                sqliteConnection.execute(f'''UPDATE SNIPERBOT SET SNIPES = SNIPES + 1 WHERE ID = "{sniper_id}"''')
                sqliteConnection.commit()
                
                #kills for the sniper

                #update the sniper counts for the people here, if not in the database , then insert new entry and then update, if alrteady in just update 
                currentScore = []
                for id in listIDsniped:
                    userHereSniped = sqliteConnection.execute(f'''SELECT EXISTS(SELECT 1 FROM SNIPERBOT WHERE ID = "{id}");''')
                    userHereListSniped = [ x for x in userHereSniped]
                    print(userHereListSniped)
                    userHerefinalSniped = userHereListSniped[0][0]
                    
                    if not userHerefinalSniped:
                        data_to_insertSniped = [(id, 0, 0)]
                        sql_querySniped = "INSERT INTO SNIPERBOT (ID, SNIPES, SNIPPED) VALUES (?, ?, ?)"
                        cursor.executemany(sql_querySniped, data_to_insertSniped)
                    
                    sqliteConnection.execute(f"UPDATE SNIPERBOT SET SNIPPED = SNIPPED + 1 WHERE ID = {id}")    
                    sqliteConnection.commit()
                    
                    #snipped count retrival -> getting values 
                    sniped_count = sqliteConnection.execute(f"SELECT SNIPPED FROM SNIPERBOT WHERE ID = {id}") 
                    snipedValue = [ x for x in sniped_count]
                    currentScore.append(snipedValue[0][0])
                
                #sniper counts retrival 
                
                score_dict = {name: score for name, score in zip(listNamesSniped, currentScore)}
                
                sniper_count = sqliteConnection.execute(f"SELECT SNIPES FROM SNIPERBOT WHERE ID = {sniper_id}")
                result = [z for z in sniper_count] 
                print(result)
                print("result for sniper count from graph: ", result[0][0])
                sniper_count_value = result[0][0]  # Assuming SNIPES is the second column in the SELECT query
                
                sniperMessage = f"{sniper} sniped {sniped_names}.\n{sniper} has sniped `{sniper_count_value}` times!! \n"
                snipedMessage = ""
                for x,y in score_dict.items():
                    snipedMessage += f"{x} has been sniped `{y}` times.\n"
                
                totalMessage = sniperMessage + snipedMessage
                await message.channel.send(totalMessage)
            else:
                await message.channel.send(f"Can't snipe without a photo lols")
                return
        
        
        
    bot.run(DISCORD_API_TOKEN) #remove this and ENV it later 


if __name__ == "__main__":
    run() 