import asyncio


async def async_sleep(duration):
    await asyncio.sleep(duration)
    return duration


async def main():
    pending = set()
    for i in range(1, 11):
        pending.add(asyncio.create_task(async_sleep(i)))

    while len(pending) > 0:
        # like processing in chunks
        done, pending = await asyncio.wait(pending, timeout=2)  # every 2 seconds we are going to have responses
        print(f"Done {done}")
        print(f"Pending {pending}")

        # we can continue adding task 
        # pending.add(asyncio.create_task(async_sleep(i)))


if __name__ == "__main__":
    asyncio.run(main())
