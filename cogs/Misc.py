import aiohttp
import asyncio
import discord
from discord.ext import commands
from PIL import Image
from PIL import ImageOps
import async_timeout
import os

class misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def img(self, ctx):
        await ctx.send("Please refer to the help command for a list of subcommands.")

    async def download_img(self, ctx, url, name):
        """Downloads an img from passed url."""
        with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    if r.status == 200:
                        with open(name, 'wb') as fp:
                            fp.write(await r.read())
                    else:
                        await ctx.send("Failed to download image.")

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
            await self.download_img(ctx, url, img_name)
        except asyncio.TimeoutError:
            await ctx.send("Image is too big.")
            os.remove(img_name)
            return

        # Invert the image
        try:
            image = Image.open(img_name)
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

def setup(bot):
    bot.add_cog(misc(bot))
