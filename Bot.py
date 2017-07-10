import discord
from discord.ext import commands
import json
import time

# Get top secret bot token
with open("APIKey.json") as f:
    API = json.load(f)

# Prefix used to interact with the bot
bot_prefix = "?"
bot_token = API['Token']
bot_description = """An all-purpose bot written for the Hopson community server."""

startup_extensions = ["cogs.member",
                      "cogs.rng",
                      "cogs.admin",
                      "cogs.challenge",
                      "cogs.misc",
                      "cogs.vote",
                      "cogs.roles",]
bot = commands.Bot(command_prefix = bot_prefix, description = bot_description)
bot.remove_command("help")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name="Type "+bot_prefix+"help"))

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
    if bot.get_cog(extension_name[extension_name.rfind(".")+1:]):
        bot.unload_extension(extension_name)
        await ctx.send("{} was successfully unloaded.".format(extension_name))

    else:
        await ctx.send("Could not unload {}, module not found.".format(extension_name))

@unload.error
async def unload_error(ctx, error):
    """Handle load's errors"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: {}unload(<extension name>).".format(bot_prefix))
    if isinstance(error, commands.errors.NotOwner):
        await ctx.send("You're not my daddy, only daddy can use this function.")


@bot.command()
async def hello(ctx):
    """Ping command"""
    await ctx.send("world.")


@bot.command()
async def help(ctx):
    """Display a message with the latest changelog and current commands."""
    msg = discord.Embed(
        title="Welcome to HopBot's help page!",
        colour=discord.Color.red(),
        description="\nChangelog:\n"
                      "\n1. Fixed a bug were I was greeting users in the wrong channel.\n"
                      "2. You can now invert images. more img related commands coming soon.\n"
                      "3. A vote module where you can ask yes or no questions, or create a poll has finally been added!\n"
                      "\n\n__**Normies Commands list:**__\n\n"

    )
    msg.add_field(
        name="coinflip:",
        value="Enter heads or tails to see what you get!\n" +
                "Usage: {}coinflip choice. coinflip is a 50/50 head or tails game.\n".format(bot_prefix),
        inline=False
    )
    msg.add_field(
        name="challenge0:",
        value="challenge0 is a command you can use to test your solution to this week's programming challenge!" +
                "\nUsage: {}challenge0 <required input>. NOTE: The maximum value allowed for either integers is 30.\n".format(bot_prefix),
        inline=False
    )
    msg.add_field(
        name="flip:",
        value="Spits out heads or tails.\n" +"Usage: {}flip <no arguments needed>.\n".format(bot_prefix),
        inline=False
    )
    msg.add_field(
        name="hello:",
        value="hello is basically a ping functions. It take no arguments.\n",
        inline=False
    )
    msg.add_field(
        name = "help:",
        value="Display this menu.\n",
        inline=False
    )
    msg.add_field(
        name="img:",
        value="img is a command that's used to add effects to images.\n" +
              "__Subcommands__:\n" +
              "   **1. invert: inverts the colours of a certain image. You can tag your friends to invert their avatars,**" +
              " **or use an image's url.**\n" +
              "         Usage: {}img invert <url or mentioned user>.\n".format(
                  bot_prefix),
        inline=False
    )
    msg.add_field(
        name="roles:",
        value="roles is used to either add or remove specified roles from the caller. You can call roles without " +
                "any subcommands to get a list of available roles.\n"+
                "__Subcommands__:\n" +
                "   **1. add: adds specified roles.**\n"+
                "       Usage: {}roles add <roles>\n".format(bot_prefix) +
                "   **2. remove: removes specified roles.**\n" +
                "       Usage: {}roles add <roles>\n".format(bot_prefix),
        inline=False
    )
    msg.add_field(
        name = "userinfo:",
        value="Mention a user to get their Discord information.".format(bot_prefix) +
                "\nUsage: {}userinfo <mentioned user>.\n".format(bot_prefix),
        inline=False
    )
    msg.add_field(
        name="vote:",
        value="Vote is a command that's used to create polls.\n" +
              "__Subcommands__:\n" +
              "   **1. poll: Creates a poll(duh) where people can vote using reactions.**\n" +
              "         Usage: {}vote poll <choices>. **NOTE:** The maximum number of choices allowed is 10.\n".format(bot_prefix) +
              "   **2. YN: Creates a question where people can vote 'yes' or 'no' to, also using reactions.**\n" +
              '         Usage: {}YN <Question>.\n'.format(bot_prefix),
        inline=False
    )
    msg.add_field(
        name="\u200b",
        value="__**Admins Commands list:**__",
        inline=False
    )
    msg.add_field(
        name="delete:",
        value="delete is a command that's used to either delete a certain member's messages, or n amount of messages inside a channel.\n" +
                "In order to use any of these feature, you'll have to use one of the two subcommands:\n" +
                "   **1. msg: deletes n amount of messages.**\n" +
                "         Usage: {}delete msg <number of messages>.\n".format(bot_prefix) +
                "   **2. usermsg: deletes n amount of messages for a mentioned user.**\n"+
                "         Usage: {}delete usermsg <mentioned user> <number of messages>.".format(bot_prefix),
        inline=False
    )
    msg.set_author(
        name="Hopbot",
        icon_url="https://cdn.pixabay.com/photo/2016/08/29/08/54/camel-1627701_960_720.jpg",
        url="https://github.com/JW999/DGBot"
    )
    msg.set_footer(
        text ="Made by JW999 and Jackojc. https://github.com/JW999/DGBot",
        icon_url="https://cdn.pixabay.com/photo/2016/08/29/08/54/camel-1627701_960_720.jpg"
    )
    msg.set_thumbnail(
        url="https://cdn.pixabay.com/photo/2016/08/29/08/54/camel-1627701_960_720.jpg"
    )

    await ctx.send(embed=msg)


if __name__ == "__main__":
    print("Loading modules....")
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    print("Connecting to Discord....")

    bot.run(bot_token)
