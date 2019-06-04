import aiohttp
import asyncio
import async_timeout

async def save_file(url, name):
    """Downloads a file and saves it on disk."""
    with async_timeout.timeout(10):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(name, 'wb') as fp:
                        fp.write(await resp.read())
                else:
                    await ctx.send("Failed to download file.")

async def download_file(url):
    """Downloads a file, but doesn't save it on disk."""
    with async_timeout.timeout(10):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    binaryData =  await resp.read()
                    return binaryData
                else:
                    await ctx.send("Failed to download file.")

async def download_json_file(url):
    """Downloads a json file, but doesn't save it on disk."""
    with async_timeout.timeout(10):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    jsonFile =  await resp.json()
                    return jsonFile
                else:
                    await ctx.send("Failed to download file.")
