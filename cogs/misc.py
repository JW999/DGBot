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


from .helpers import filedownloader
from .helpers import jsonTest
import asyncio
import async_timeout
import discord
from discord.ext import tasks, commands
import os
from PIL import Image
from PIL import ImageOps
import json
import praw
import random

class InvalidLinkError(Exception):
    pass


class reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Get top secret reddit credentials
        reddit_creds = jsonTest.import_data("data")
        self.reddit = praw.Reddit(client_id=reddit_creds["Reddit"]["client_id"],
                                  client_secret=reddit_creds["Reddit"]["client_secret"],
                                  username=reddit_creds["Reddit"]["username"],
                                  password=reddit_creds["Reddit"]["password"],
                                  user_agent='Meme script by JW999')
        self.linkGenerators = {}
        self.make_generators()

    @commands.group(invoke_without_command=True)
    async def memes(self, ctx):
        await ctx.send("Please refer to the help command for a list of subcommands.")

    @memes.command()
    async def send(self,ctx, subreddit_choice=None):
        '''A wrapper function around `upload_picture`'''
        if subreddit_choice is None:
            subreddit = random.choice(("dankmemes", "memes"))
        elif subreddit_choice =="science":
            subreddit = "sciencememes"
        else:
            return await ctx.send("Bad argument, can only provide science as an argument")

        try:
            link =  next(self.linkGenerators[subreddit])
            print(link)
            await self.upload_picture(ctx, link)
        except StopIteration:
            self.reset_link_generator(subreddit)
            await ctx.invoke(ctx.command, subreddit_choice)
        except InvalidLinkError:
            print("invalid link was triggered.")
            await ctx.invoke(ctx.command, subreddit_choice)

    async def upload_picture(self, ctx, link):
        ''' Check the source and format of the picture. Save it on disk,
            send it, then delete it. If an invalid link was passed, raise
            InvalidLinkError() '''

        if 'i.redd.it' in link or 'i.imgur.com' in link:
            file_format = link.rsplit(".", 1)[1]
            if 'jpg' in file_format or 'png' in file_format or 'jpeg' in file_format:
                file_name = link.rsplit("/", 1)[1]
                await filedownloader.save_file(link, "binary", file_name)
                await ctx.send(file=discord.File(file_name))
                os.remove(file_name)
        else:
            raise InvalidLinkError()

    def make_generators(self):
        ''' Inititializes 'link generators' with generators for subreddits
            saved in subreddits.txt.
        '''

        with open("assets/subreddits.txt", "r") as fp:
            subredditNames = fp.read().splitlines()

        for subredditName in subredditNames:
            self.linkGenerators[subredditName] = self.make_link_generator(subredditName)

    def make_link_generator(self, subreddit:str):
        ''' Return a generator that generates reddit post links using
            "PRAW: Python Reddit API Wrapper" library.
        '''

        for submission in self.reddit.subreddit(subreddit).hot():
            if not submission.stickied:
                yield submission.url

    @tasks.loop(hours=24)
    async def reset_link_generator_task(self):
        ''' background task to reset generators'''
        self.reset_link_generator()

    def reset_link_generator(self, subreddit=None):
        ''' create a new link generator, because:
            1. The genetaor raised StopIteration exception and this method
                was excplicity called.
            2. Automatically called by a background task(every 24 hours).
        '''
        if subreddit is None:    # Not empty
            self.linkGenerators[subreddit[0]] = self.make_link_generator(subreddit[0])
        else:             # ran as an automatic background task
            self.make_generators()

def setup(bot):
    bot.add_cog(misc(bot))
    bot.add_cog(reddit(bot))

def teardown(bot):
    bot.remove_cog(misc(bot))
    bot.remove_cog(reddit(bot))
