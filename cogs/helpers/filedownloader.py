import aiohttp
import asyncio
import async_timeout

async def save_file(ctx, url, name):
    """Downloads file and saves it on disk."""
    with async_timeout.timeout(10):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    with open(name, 'wb') as fp:
                        fp.write(await r.read())
                else:
                    await ctx.send("Failed to download file.")

async def download_file(ctx, url):
    """Downloads file but doesn't save it on disk."""
    with async_timeout.timeout(10):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    return await r.read()
                else:
                    await ctx.send("Failed to download file.")
