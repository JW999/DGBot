import aiohttp
import asyncio
import async_timeout

async def save_file(url:str, dataType:str, filename:str):
    """Saves file returned by download_file to disk.
        Similar to Download_file dataType determines whether to retreive 'json'(decoded into a dict), 'text', or 'binary' data."""
    downloadedData = await download_file(url, dataType)

    try:
        if dataType == 'binary':
            with open(f"{filename}", "wb") as f:
                print(filename)
                f.write(downloadedData)
        elif dataType == 'text':
            with open(f"{filename}.txt", "w") as f:
                f.write(downloadedData)
        elif dataType == 'json':
            decodedJsonDict =  await resp.json()
            with open(f"{filename}.json", "w") as f:
                json.dump(data, f, indent=4)
        else:
            print("Invalid dataType. Check function's doc string.")
    except Exception as exp:
        exc = f'{type(exp).__name__}: {exp}'
        print(f'Failed to save file. {exc}. Show this to someRandomeName')


async def download_file(url:str, dataType:str):
    """Downloads a file, but doesn't save it on disk.
        dataType determines whether to retreive 'json'(decoded into a dict), 'text', or 'binary' data."""
    try:
        with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        ### Output depends on dataType ###
                        if dataType == 'binary':
                            binaryData =  await resp.read()
                            return binaryData
                        elif dataType == 'text':
                            textData =  await resp.text()
                            return textData
                        elif dataType == 'json':
                            decodedJsonDict =  await resp.json()
                            return binaryData
                        else:
                            print("Invalid dataType. Check function's doc string.")
                    else:
                        print("Failed to download file.")
    except Exception as exp:
        exc = f'{type(exp).__name__}: {exp}'
        print(f'Failed to download file. {exc}. Show this to someRandomeName')
        # await ctx.send(f'Failed to save file {exc}. Show this to someRandomeName')
