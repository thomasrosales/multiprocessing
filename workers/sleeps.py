import time
from threading import Thread


class SleepyWorker(Thread):

    def __init__(self, seconds, **kwargs):
        super().__init__(**kwargs)
        self._seconds = seconds
        self.start()

    def _sleep_a_little(self):
        time.sleep(self._seconds)

    def run(self):
        self._sleep_a_little()
