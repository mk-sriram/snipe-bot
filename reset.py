import sqlite3

sqliteConnection = sqlite3.connect('SniperBot.db')
cursor = sqliteConnection.cursor()
print ("Opened database successfully")


sqliteConnection.execute('''DELETE FROM SNIPERBOT''')
print("deleted successfully")

