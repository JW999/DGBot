import discord
from discord.ext import commands
import asyncio
import random

# Prefix used to interact with the bot
bot_prefix = "?"
bot_token = "Get your own token!!!"
bot_description = """A bot that greets new users, for now."""


bot = commands.Bot(command_prefix = bot_prefix, description = bot_description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name="Type " + bot_prefix + "help"))

@bot.event
async def on_member_join(member):
    msg = "Hello and welcome to the best C++/game dev server on Discord!!! {}".format(member.mention)
    await member.guild.default_channel.send(msg)

@bot.command()
async def hello(ctx):
    """Says world"""
    await ctx.send("world")

@bot.command()
async def add(ctx, left : int, right : int):
    """Adds two numbers together."""
    try:
        await ctx.send(left + right)
    except ValueError:
        await ctx.send("Invalid input")

@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Invalid input")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Invalid input")

@bot.command()
async def coinflip(ctx, choice : str):
    """A fair 50/50 coin flip"""
    choices = ["heads", "tails"]
    number = random.randint(1,2)
    if choice.lower() in choices:
        if choice.lower() == choices[number - 1].lower():
            await ctx.send("Yep that's right, you got {}".format(choices[number - 1].title()))
        else:
            await ctx.send("You got rick rolled.")
    else:
        await ctx.send("Are you trying to break me? Bastard :triumph:")

@coinflip.error
async def add_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Where's your input at?")

bot.run(bot_token)