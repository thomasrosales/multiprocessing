import asyncio
import time

import aiohttp
import requests


# async function

async def async_sleep(n):
    # time.sleep(5)
    print(f"Before sleep {n}")
    await asyncio.sleep(n)  # coroutine
    print(f"After sleep {n}")


async def async_sleep_generator(n):
    print(f"Before sleep {n}")
    n = max(2, n)
    for i in range(1, n):
        yield i
        await asyncio.sleep(i)  # coroutine
    print(f"After sleep {n}")


async def greeting():
    print("hello")
    return "Hola"


async def main():
    # Blocking calls among awaits
    start = time.time()
    task = asyncio.create_task(async_sleep(1))  # Schedule the execution of a coroutine object in a spawn task
    await async_sleep(2)
    await task
    await greeting()
    print(f"Total time: {time.time() - start}")


async def main2():
    # runs concurrently
    start = time.time()
    await asyncio.gather(async_sleep(2), async_sleep(1), greeting())  # schedules and executes tasks concurrently
    print(f"Total time: {time.time() - start}")


async def main3():
    start = time.time()
    # if there is a TimeoutError is going to interrupt the other tasks
    try:
        await asyncio.gather(asyncio.wait_for(async_sleep(20), 5), async_sleep(1), greeting())
    except TimeoutError as err:
        print(f"Error: {str(err)}")
    print(f"Total time: {time.time() - start}")


async def main4():
    start = time.time()
    # with for statement it continues being sequentially
    async for k in async_sleep_generator(5):
        print(k)
    print(f"Total time: {time.time() - start}")


async def main5():

    async def get_url_response(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    # other libraries
    urls = [
        "https://google.com",
        "https://docs.python.org/3/library/asyncio.html",
        "https://stackoverflow.com/questions/8561470/sqlalchemy-filtering-by-relationship-attribute",
        "https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.update",
        "https://docs.python.org/3/library/concurrency.html"
    ]
    start = time.time()

    sync_response = []
    for url in urls:
        sync_response.append(requests.get(url).text)

    print(f"Sync -> Total time: {time.time() - start}")

    start = time.time()

    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(get_url_response(url)))

    async_text_response = await asyncio.gather(*tasks)

    print(f"Async -> Total time: {time.time() - start}")


if __name__ == '__main__':
    # With async runs single core in a single thread, but you can
    # achieve concurrency. In web applications you usually will use
    # async operations
    asyncio.run(main5())  # entrypoint to out program
