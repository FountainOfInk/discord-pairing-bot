import discord
from extbot import Bot

intents = discord.Intents.all()
intents.members = True
intents.presences = True
bot = Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    

bot.load_extension("helpers")
bot.load_extension("real")
bot.load_extension("debugging")

bot.run("REPLACEME")
