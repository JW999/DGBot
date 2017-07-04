import discord
from discord.ext import commands
from random


class random:
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
                await ctx.send("You got rick rolled.")
        else:
            await ctx.send("Are you trying to break me? Bastard :triumph:")

    @coinflip.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Where's your input at?")


def setup(bot):
    bot.add_cog(random(bot))