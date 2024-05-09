import asyncio
import multiprocessing


class MultiprocessingAsync(multiprocessing.Process):

    def __init__(self, durations):
        super().__init__()
        self._durations = durations

    @staticmethod
    async def async_sleep(duration):
        await asyncio.sleep(duration)
        return duration

    async def consecutive_sleeps(self):
        pending = set()
        for i in self._durations:
            pending.add(asyncio.create_task(self.async_sleep(i)))

        while len(pending) > 0:
            done, pending = await asyncio.wait(pending, timeout=1)
            for done_task in done:
                print(await done_task)

    def run(self):
        asyncio.run(self.consecutive_sleeps())
        print(f"{self} finished")


if __name__ == "__main__":
    processes = [MultiprocessingAsync([5, 3, 1, 2, 6]) for i in range(2)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
