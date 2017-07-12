import discord
from discord.ext import commands
import random
import asyncio


class admin:
    """This class includes admin only commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def delete(self, ctx):
        await ctx.send("Check the help page for a list of subcommands")

    @delete.command()
    @commands.has_permissions(administrator=True)
    async def usermsg(self, ctx, name: str, number_messages: int):
        """Delete n messages for a mentioned user"""
        if number_messages < 1:
            await ctx.send("Erm, what exactly am I exactly supposed to delete?")
            return
        user = ctx.message.mentions[0]  # Get the mentioned user

        async for message in ctx.channel.history(limit=1000):
            if ctx.message.id == message.id:
                continue
            if message.author.id == user.id:
                if number_messages != 0:
                    number_messages -= 1
                    await message.delete()
                else:
                    break

        await ctx.message.delete()

    @usermsg.error
    async def usermsg_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument) or isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Check the help page for usage instructions.")
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You're not an admin.")

    @delete.command()
    @commands.has_permissions(administrator=True)
    async def msg(self, ctx, number_messages :int):
        """Deletes n messages from a channel"""
        if number_messages < 1:
            await ctx.send("Erm, what exactly am I exactly supposed to delete?")
            return
        number_messages += 2  # to account for the calling message
        await ctx.send(file=discord.File(f"assets/Men-in-Black{random.randint(1, 3)}.png"))
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=number_messages)

    @msg.error
    async def msg_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument) or isinstance(error,commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Check the help page for usage instructions.")
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You're not an admin.")


def setup(bot):
    bot.add_cog(admin(bot))