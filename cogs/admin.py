import discord
from discord.ext import commands

class adminCommands:
    """This class includes admin only commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def delete (self, ctx):
        await ctx.send("Check the help page for a list of subcommands")

    @delete.command()
    @commands.has_permissions(administrator=True)
    async def usermsg(self, ctx, name: str, n: int):
        """Delete n messages for a mentioned user"""
        user = ctx.message.mentions[0]  # Get the mentioned user
        number_messages = n

        async for message in ctx.channel.history(limit=1000):
            if ctx.message.id == message.id:
                continue
            if message.author.id == user.id and number_messages != 0:
                number_messages -= 1
                await message.delete()
            else:
                break

        await ctx.message.delete()

    @usermsg.error
    async def usermsg_error(ctx, error):
        if isinstance(error, commands.errors.BadArgument) or isinstance(error,commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Check the help page for usage instructions.")
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You're not an admin.")


    @delete.command()
    @commands.has_permissions(administrator=True)
    async def msg(self, ctx, n :int):
        """Deletes n messages for a mentioned user"""
        number_messages = n

        async for message in ctx.channel.history(limit=1000):
            if ctx.message.id == message.id:
                continue
            if number_messages != 0:
                number_messages -= 1
                await message.delete()
            else:
                break

        await ctx.message.delete()

    @msg.error
    async def msg_error(ctx, error):
        if isinstance(error, commands.errors.BadArgument) or isinstance(error,commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Check the help page for usage instructions.")
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You're not an admin.")



def setup(bot):
    bot.add_cog(adminCommands(bot))