import discord
from discord.ext import commands
import asyncio

# Prefix used to interact with the bot
bot_prefix = "?"
bot_token = "MzMwNDczNDM4MjI3NDY0MTky.DDhhBw.NLI31T6GlQ4CWj4GoLWJxsQnBiw"
bot_description = """A bot that greets new users, for now."""


my_bot = commands.Bot(command_prefix = bot_prefix)

@bot.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@bot.command()
async def hello():
    """Says world"""
    await bot.say("world")

bot.run(bot_token)