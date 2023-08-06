import asyncio
import atexit
import warnings
import aiohttp
import nest_asyncio

warnings.filterwarnings("ignore", category=DeprecationWarning)

session = aiohttp.ClientSession()

async def closer():
    nest_asyncio.apply()
    await session.close()

def closer_run():
    asyncio.run(closer())

def get(url):
    """
    aiohttp_but_its_requests.get(url)
    Returns a ClientResponse object.
    """
    async def geturl():
        async with session.get(url) as response:
            global RETURNED
            RETURNED = response
            # await session.close()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(geturl())
    return RETURNED

def post(url, data):
    """
    aiohttp_but_its_requests.post(url, data)
    Returns a ClientResponse object.
    """
    async def geturl():
        async with session.post(url, data=data) as response:
            global RETURNED
            RETURNED = response
            # await session.close()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(geturl())
    return RETURNED

def delete(url):
    """
    aiohttp_but_its_requests.delete(url)
    Returns a ClientResponse object.
    """
    async def deleteurl():
        async with session.delete(url) as response:
            global RETURNED
            RETURNED = response
            # await session.close()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(deleteurl())
    return RETURNED

def head(url):
    """
    aiohttp_but_its_requests.head(url)
    Returns a ClientResponse object.
    """
    async def headurl():
        async with session.head(url) as response:
            global RETURNED
            RETURNED = response
            # await session.close()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(headurl())
    return RETURNED

def options(url):
    """
    aiohttp_but_its_requests.options(url)
    Returns a ClientResponse object.
    """
    async def optionsurl():
        async with session.options(url) as response:
            global RETURNED
            RETURNED = response
            # await session.close()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(optionsurl())
    return RETURNED

atexit.register(closer_run)