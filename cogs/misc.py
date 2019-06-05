from .helpers import filedownloader
import asyncio
import async_timeout
import discord
from discord.ext import tasks, commands
import os
from PIL import Image
from PIL import ImageOps
import json
import praw

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def img(self, ctx):
        await ctx.send("Please refer to the help command for a list of subcommands.")

    @img.command()
    async def invert(self, ctx, url :str):
        if not ctx.message.mentions:
            if not url:
                url = ctx.message.author.avatar_url
            else:
                pass
        else:
            url = ctx.message.mentions[0].avatar_url

        # Download the image
        img_name = "{}.png".format(url[url.rfind("/")+1:url.rfind(".")])
        try:
            await filedownloader.save_file(url, "binary", img_name)
        except asyncio.TimeoutError:
            await ctx.send("Image is too big.")
            os.remove(img_name)
            return
        except ValueError:
            await ctx.send("Invalid link.")
            return

        # Invert the image
        try:
            image = Image.open(img_name)

            width, height = image.size
            if (width * height) > 89478485:  # Checks if image is too big
                await ctx.send("Image is too big.")
                os.remove(img_name)
                return

            if image.mode == "RGBA":
                image.load()
                r, g, b, a = image.split()
                image = Image.merge("RGB", (r, g, b))
                image = ImageOps.invert(image)
                r, g, b = image.split()
                image = Image.merge("RGBA", (r, g, b, a))
            else:
                image = ImageOps.invert(image)
        except NotImplementedError:
            await ctx.send("Image format not supported.")
            os.remove(img_name)
            return
        except OSError:
            await ctx.send("Link not supported.")
            os.remove(img_name)
            return


        image.save(img_name)
        await ctx.channel.send(file=discord.File(img_name))
        os.remove(img_name)

    @invert.error
    async def inver_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Are you expecting me to make an image out of thin air?")


class reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Get top secret reddit credentials
        with open("data.json") as f:
            reddit_creds = json.load(f)
        self.reddit = praw.Reddit(client_id=reddit_creds["Reddit"]["client_id"],
                                  client_secret=reddit_creds["Reddit"]["client_secret"],
                                  username=reddit_creds["Reddit"]["username"],
                                  password=reddit_creds["Reddit"]["password"],
                                  user_agent='Meme script by JW999')

        self.dankHotLinkGenerator =  self.memeLinkHotGenerator('dankmemes')
        self.dankTopLinkGenerator =  self.memeLinkTopGenerator('dankmemes')

    @commands.group(invoke_without_command=True)
    async def memes(self, ctx):
        await ctx.send("Please refer to the help command for a list of subcommands.")

    @memes.command()
    async def dank(self,ctx):
        try:
            link =  next(self.dankHotLinkGenerator)
            await self.send_picture(ctx, link)
        except StopIteration:
            self.dankHotLinkGenerator = await self.memeLinkHotGenerator('dankmemes')
            await self.dank(ctx)

    @memes.command()
    async def top_dank(self,ctx):
        try:
            link =  next(self.dankTopLinkGenerator)
            await self.send_picture(ctx, link)
        except StopIteration:
            self.dankTopLinkGenerator = await self.dankTopLinkGenerator('dankmemes')
            await self.top_dank(ctx)


    async def send_picture(self, ctx, link):
        # make sure: reddit image, not gif.
        if 'i.redd.it' in link:
            file_format = link.rsplit(".", 1)[1]
            if 'jpg' in file_format or 'png' in file_format or 'jpeg' in file_format:
                file_name = link.rsplit("/", 1)[1]
                await filedownloader.save_file(link, "binary", file_name)
                await ctx.send(file=discord.File(file_name))
                os.remove(file_name)
        else:
            self.dank(ctx) # Try another link


    def memeLinkHotGenerator(self, subreddit:str):
        for submission in self.reddit.subreddit(subreddit).hot():
            if not submission.stickied:
                yield submission.url

    def memeLinkTopGenerator(self, subreddit:str):
        for submission in self.reddit.subreddit(subreddit).top('day'):
            if not submission.stickied:
                yield submission.url

    @tasks.loop(hours=1.0)
    async def resetHotGenerator(self):
        self.dankHotLinkGenerator = await self.memeLinkHotGenerator('dankmemes')

    @tasks.loop(hours=24.0)
    async def resetTopGenerator(self):
        self.dankTopLinkGenerator = await self.memeLinkTopGenerator('dankmemes')


def setup(bot):
    bot.add_cog(misc(bot))
    bot.add_cog(reddit(bot))

def teardown(bot):
    bot.remove_cog(misc(bot))
    bot.remove_cog(reddit(bot))
