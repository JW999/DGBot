from .helpers import filedownloader
import asyncio
import async_timeout
import discord
from discord.ext import commands
import os
from PIL import Image
from PIL import ImageOps
import json

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
            await filedownloader.save_file(url, img_name)
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


class memes(commands.Cog):
    """A class that sends memes from reddit, maybe bobs later."""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def memes(self, ctx):
        await ctx.send("I still haven't added commands to the help page, as Husam about them.")

    @memes.command()
    async def topDank(self, ctx):
        """Downloads the top meme of the day from /r/dankmemes"""
        name = "top.json"
        url = "https://www.reddit.com/r/dankmemes/top.json"

        try:
            redditData = await filedownloader.download_json_file(url)
        except asyncio.TimeoutError:
            await ctx.send("A connection error has occured.")
            return

        #first_post = redditData[0]['data']
        #image_url = first_post['url']
        #redditData = json.loads(json.dumps(redditData))
        img_url = redditData['data']['children'][0]['data']['url']

        img_name = "{}.png".format(img_url[img_url.rfind("/")+1:img_url.rfind(".")])
        try:
            await filedownloader.save_file(img_url, img_name)
        except asyncio.TimeoutError:
            await ctx.send("Image is too big.")
            os.remove(img_name)
            return
        except ValueError:
            await ctx.send("Invalid link.")
            return
        await ctx.channel.send(file=discord.File(img_name))
        os.remove(img_name)





def setup(bot):
    bot.add_cog(misc(bot))
    bot.add_cog(memes(bot))
