import discord
from discord.ext import commands
import random


class rng:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinflip(self, ctx, choice: str):
        """A fair 50/50 coin flip"""
        choices = ["heads", "tails"]
        number = random.randint(1, 2)
        if choice.lower() in choices:
            if choice.lower() == choices[number - 1].lower():
                await ctx.send("Yep that's right, you got {}".format(choices[number - 1].title()))
            else:
                await ctx.send("Nope.")
        else:
            await ctx.send("Are you trying to break me? Bastard :triumph:")

    @coinflip.error
    async def coinflip_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Input please?")


    @commands.command()
    async def flip(self, ctx):
        "Fair 50/50 heads or tails"
        number = random.randint(1, 2)

        if number == 1:
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")


def setup(bot):
    bot.add_cog(rng(bot))