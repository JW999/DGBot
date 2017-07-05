import discord
from discord.ext import commands

# Prefix used to interact with the bot
bot_prefix = "?"
bot_token = "MzMwNDczNDM4MjI3NDY0MTky.DDwyTQ.IHLJIbl1Kxu-LRVhoPjyKs9wPC8"
bot_description = """An all-purpose bot written for the Hopson community server."""

startup_extensions = ["cogs.members",
                      "cogs.RNG",
                      "cogs.admin",
                      "cogs.challenge"]
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
                      "\n1. Added a help function.\n"
                      "2. You can now use the challenge command to test your challenge solutions!\n"
                      "3. You can now use the userinfo command to get someone's Discord information!(Ty NSA shhhh!)\n"
                      "4. Admins can now delete a certain member's messages automatically.(You're welcome ;) )"
                      "\n\n__**Commands list:**__\n\n",

    )
    msg.add_field(
        name = "add:",
        value = "Usage: ?add int1 in2. Adds 2 integer, duh.",
        inline = False,
    )
    msg.add_field(
        name = "coinflip:",
        value = "Usage: {}coinflip choice. coinflip is a 50/50 head or tails game.\n".format(bot_prefix) +
                "Enter heads or tails to see what you get!",
        inline = False,
    )
    msg.add_field(
        name="[Admins only]deletemsg",
        value="Usage: {}deletemsg @<member> <number of messages>.\nDelete <number of messages> for <member>.".format(bot_prefix),
        inline=False,
    )
    msg.add_field(
        name = "hello:",
        value = "hello is basically a ping functions. It take no arguments.",
        inline = False,
    )
    msg.add_field(
        name = "help",
        value = "Display this menu.",
        inline = False,
    )
    msg.add_field(
        name = "userinfo:",
        value = "Usage: {}userinfo @user.\n".format(bot_prefix) + "Mention a user to get their Discord information.".format(bot_prefix),
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
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(bot_token)