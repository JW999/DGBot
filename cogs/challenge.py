"""This module includes solutions to all of the programming challenges on Hopson's community server."""
import discord
from discord.ext import commands
import random
import itertools
import math

class challenge:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def challenge0(self, ctx, n: int, s: int):
        if n > 30 or s > 30:
            await ctx.send("Don't break me plox")
            return
        summ = 0
        # is prime
        if s > 1 and all(s % i for i in itertools.islice(itertools.count(2), int(math.sqrt(s) - 1))):
            for k in range(0, n + 1):
                if k > 1 and all(k % i for i in itertools.islice(itertools.count(2), int(math.sqrt(k) - 1))):
                    summ += k
        else:
            # is even
            if s % 2 == 0:
                for i in range(0, n + 1):
                    if i % 2 == 0:
                        summ += i
            else:
                for i in range(0, n + 1):
                    if i % 2 != 0:
                        summ += i
        await ctx.send(summ)

def setup(bot):
    bot.add_cog(challenge(bot))