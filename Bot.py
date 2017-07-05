import discord
from discord.ext import commands
import time

# Prefix used to interact with the bot
bot_prefix = "?"
bot_token = "MzMwNDczNDM4MjI3NDY0MTky.DDwyTQ.IHLJIbl1Kxu-LRVhoPjyKs9wPC8"
bot_description = """An all-purpose bot written for the Hopson community server."""

startup_extensions = ["cogs.members",
                      "cogs.RNG",
                      "cogs.admin",
                      "cogs.challenge",
                      "cogs.Misc"]
bot = commands.Bot(command_prefix = bot_prefix, description = bot_description)
bot.remove_command("help")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name="Type " + bot_prefix + "help"))

@bot.command()
@commands.is_owner()
async def load(ctx, extension_name :str):
    """Load an extension"""
    bot.load_extension(extension_name)
    await ctx.send("{} was successfully loaded.".format(extension_name))

@load.error
async def load_error(ctx, error):
    """Handle load's errors"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: {}load(<extension name>).".format(bot_prefix))
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Module not found.")
    if isinstance(error, commands.errors.NotOwner):
        await ctx.send("You're not my daddy, only daddy can use this function.")

@bot.command()
@commands.is_owner()
async def unload(ctx, extension_name :str):
    bot.unload_extension(extension_name)
    await ctx.send("{} was successfully unloaded.".format(extension_name))


@bot.command()
async def hello(ctx):
    """Ping command"""
    ctx.send("world.")


@bot.command()
async def help(ctx):
    """Display a message with the latest changelog and current commands."""
    msg = discord.Embed(
        title = "Welcome to DGBot's help page!",
        colour = 0xe74c3c, #red
        description = "Changelog:\n"
                      "\n1. I've added your boring generic flip command!\n"
                      "2. Admins now have 1 more message deleting option!\n"
                      "3. The bot's owner can now load and unload modules on the fly!\n"
                      "4. Much cleaner source code."
                      "\n\n__**Normie Commands list:**__\n\n",

    )
    msg.add_field(
        name = "coinflip:",
        value = "Enter heads or tails to see what you get!\n" +
                "Usage: {}coinflip choice. coinflip is a 50/50 head or tails game.\n".format(bot_prefix),
        inline = False,
    )
    msg.add_field(
        name = "challenge0:",
        value = "challenge0 is a command you can use to test your solution to this week's programming challenge!" +
                "\nUsage: {}challenge0 <required input>.".format(bot_prefix),
        inline = False
    )
    msg.add_field(
        name = "flip:",
        value = "Spits out heads or tails.\n" +"Usage: {}flip <no arguments needed>.".format(bot_prefix),
        inline = False
    )
    msg.add_field(
        name = "hello:",
        value = "hello is basically a ping functions. It take no arguments.",
        inline = False,
    )
    msg.add_field(
        name = "help:",
        value = "Display this menu.",
        inline = False,
    )
    msg.add_field(
        name = "userinfo:",
        value = "Mention a user to get their Discord information.".format(bot_prefix) +
                "\nUsage: {}userinfo <mentioned user>.".format(bot_prefix),
        inline = False,
    )
    msg.add_field(
        name = "\u200b",
        value= "__**Admin Commands list:**__",
        inline = False,
    )
    msg.add_field(
        name = "delete:",
        value = "delete is a command that's used to either delete a certain member's messages, or n amount of messages inside a channel.\n" +
                "In order to use any of these feature, you'll have to use one of the two subcommands:\n" +
                "   **1. msg: deletes n amount of messages.**\n" +
                "         Usage: {}delete msg <number of messages>.\n".format(bot_prefix) +
                "   **2. usermsg: deletes n amount of messages for a mentioned user.**\n"+
                "         Usage: {}delete usermsg <mentioned user> <number of messages>.".format(bot_prefix),
        inline = False,
    )
    msg.set_author(
        name = "DGBot",
        icon_url = "https://cdn.pixabay.com/photo/2016/08/29/08/54/camel-1627701_960_720.jpg",
        url = "https://github.com/JW999/DGBot",
    )
    msg.set_footer(
        text = "Made by JW999 and Jackojc. https://github.com/JW999/DGBot",
        icon_url = "https://cdn.pixabay.com/photo/2016/08/29/08/54/camel-1627701_960_720.jpg",
    )
    msg.set_thumbnail(
        url = "https://cdn.pixabay.com/photo/2016/08/29/08/54/camel-1627701_960_720.jpg",
    )

    await ctx.send(embed = msg)


if __name__ == "__main__":
    print("Loading modules....")
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    time.sleep(2)
    print("Connecting to Discord....")

    bot.run(bot_token)