import discord
from discord.ext import commands
import asyncio
import random
from itertools import *
from math import *

# Prefix used to interact with the bot
bot_prefix = "?"
bot_token = "user your own token"
bot_description = """A bot that greets new users, for now."""

bot = commands.Bot(command_prefix = bot_prefix, description = bot_description)
bot.remove_command("help")

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
        await ctx.send("Where's your input at?")
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

@bot.command()
async def help(ctx):
    msg = discord.Embed(
        title = "title123",
        colour = 0xe74c3c, #red
        description = "Testing...\n\n"
                      "Commands:\n"
                      "1.asdasd\n"
                      "2.asdhgasjdgsa\n"
                      "3. ashdgasjhdas\n"
                      "-------------------\n\n"
                      "This bot was created by PornstarName and Jackojc\n"
    )
    msg.set_author(
        name = "Best bot ever",
        icon_url = "https://cdn.pixabay.com/photo/2016/09/15/21/02/alpaca-1672647_960_720.jpg",
        url = "https://github.com/JW999/DGBot"
    )

    msg.add_field(
        name = "Title 2",
        value = "test 123\n"
                "test456\n",
        inline = False
    )
    msg.add_field(
        name = "Title 3",
        value = "test 123\n"
                "test456\n",
    )
    msg.add_field(
        name = "Title 4",
        value = "test 123\n"
                "test456\n",
    )

    msg.set_footer(
        text = "Made by James and Jack. https://github.com/JW999/DGBot",
        icon_url = "https://cdn.pixabay.com/photo/2016/09/15/21/02/alpaca-1672647_960_720.jpg"
    )

    msg.set_thumbnail(
        url = "https://cdn.pixabay.com/photo/2016/09/15/21/02/alpaca-1672647_960_720.jpg"
    )

    await ctx.message.delete()
    await ctx.send(embed = msg)

@bot.command()
async def challenge(ctx, n : int, s : int):
    summ = 0
    # is prime
    if s > 1 and all(s % i for i in islice(count(2), int(sqrt(s)-1))):
        for k in range(0, n+1):
            if k > 1 and all(k % i for i in islice(count(2), int(sqrt(k)-1))):
                summ += k
    else:
        #is even
        if s % 2 == 0:
            for i in range(0, n+1):
                if i % 2 == 0:
                    summ += i
        else:
            for i in range(0, n+1):
                if i % 2 != 0:
                    summ += i
    await ctx.send(summ)

bot.run(bot_token)