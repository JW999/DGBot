import discord
from discord.ext import commands
import asyncio
import random
from itertools import *
from math import *

# Prefix used to interact with the bot
bot_prefix = "?"
bot_token = "yout token here"
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
        title = "Welcome to DGBot's help page!",
        colour = 0xe74c3c, #red
        description = "Changelog:\n"
                      "\n1. Added a help function.\n"
                      "2. You can now use the challenge command to test your challenge solutions!\n"
                      "3. You can now use the userinfo command to get someone's Discord information!(Ty NSA shhhh!)\n"
                      "\n\n__**Commands list:**__\n\n",

    )
    msg.add_field(
        name = "add:",
        value = "Usage: ?add int1 in2. Adds 2 integer, duh.",
        inline = False,
    )
    msg.add_field(
        name = "coinflip:",
        value = "Usage: ?coinflip choice. coinflip is a 50/50 head or tails game.\n" +
                "Enter heads or tails to see what you get!",
        inline = False,
    )
    msg.add_field(
        name = "hello:",
        value = "hello is basically a ping functions. It take no arguments",
        inline = False,
    )
    msg.add_field(
        name = "help",
        value = "Display this menu.",
        inline = False,
    )
    msg.add_field(
        name = "userinfo:",
        value = "Usage: ?userinfo @user.\n" + "Mention a user to get their Discord information.",
        inline = False,
    )
    msg.set_author(
        name = "DGBot",
        icon_url = "https://cdn.pixabay.com/photo/2016/09/15/21/02/alpaca-1672647_960_720.jpg",
        url = "https://github.com/JW999/DGBot",
    )
    msg.set_footer(
        text = "Made by JW999 and Jackojc. https://github.com/JW999/DGBot",
        icon_url = "https://cdn.pixabay.com/photo/2016/09/15/21/02/alpaca-1672647_960_720.jpg",
    )
    msg.set_thumbnail(
        url = "https://cdn.pixabay.com/photo/2016/09/15/21/02/alpaca-1672647_960_720.jpg",
    )

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

@bot.command()
async def userinfo(ctx):
    try:
        user = ctx.message.mentions[0]
    except IndexError:
        await ctx.send("You didn't mention any users")

    usermsg = discord.Embed(
        title = ":open_file_folder: User information about {}#{}.".format(user.name, user.discriminator),
        colour = 0x9b59b6, #purple
    )
    usermsg.add_field(
        name = "Username:",
        value = user.name,
        inline = False,
    )
    usermsg.add_field(
        name = "Nickname:",
        value = user.nick,
        inline = False,
    )
    usermsg.add_field(
        name = "User ID:",
        value = user.id,
        inline = False,
    )
    usermsg.add_field(
        name = "Status",
        value = user.status,
        inline = False,
    )
    usermsg.add_field(
        name = "Joined Discord on:",
        value = str(user.created_at)[:16],
        inline = False,
    )
    usermsg.add_field(
        name = "Joined server on:",
        value = str(user.joined_at)[:16],
        inline = False,
    )
    usermsg.set_thumbnail(
        url = user.avatar_url
    )
    await ctx.send(embed = usermsg)
bot.run(bot_token)