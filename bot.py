import discord
from discord.ext import commands
import asyncio
import random

# Prefix used to interact with the bot
bot_prefix = "?"
bot_token = "MzMwNDczNDM4MjI3NDY0MTky.DDhhBw.NLI31T6GlQ4CWj4GoLWJxsQnBiw"
bot_description = """A bot that greets new users, for now."""


bot = commands.Bot(command_prefix = bot_prefix, description = bot_description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def hello():
    """Says world"""
    await bot.say("world")

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command()
async def coinflip():
    """A fair 50/50 coin flip"""
    number = random.randint(1,2)
    if number == 1:
        await bot.say("Tails")
    else:
        await bot.say("Heads")

bot.run(bot_token)