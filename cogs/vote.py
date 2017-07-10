import discord
from discord.ext import commands

class vote:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def vote(self, ctx):
        await ctx.send("Check help for a list of subcommands.")

    @vote.command()
    async def poll(self, ctx, *args):
        """A poll were people vote by reacting."""
        if len(args) < 2:
            await ctx.send("Please insert at least 2 choices.")
            return

        emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
        s = ""

        for i, option in enumerate(args):
            if i > 9:
                break

            s += "To vote for {}, react with {}.\n".format(option, emojis[i])

        embed = discord.Embed(title = "Vote now!", colour = 0xF1C40F ,description = s)
        msg = await ctx.send(embed = embed)
        for emoji in emojis[:len(args)]:
            await msg.add_reaction(emoji)

    @vote.command()
    async def YN(self, ctx, *, question):
        """A yes or no vote."""
        emojis = ['✅', '❌']

        embed = discord.Embed(title= question, colour = 0x71368A)
        msg = await ctx.send(embed = embed)
        for emoji in emojis:
            await msg.add_reaction(emoji)

    @YN.error
    async def YN_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Where's your question?")


def setup(bot):
    bot.add_cog(vote(bot))