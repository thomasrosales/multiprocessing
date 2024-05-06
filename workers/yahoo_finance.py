import random
import time
from datetime import datetime
from multiprocessing import Queue
from queue import Empty
from threading import Thread

import requests
from lxml import html


class YahooFinancePriceScheduler(Thread):  # master threading class
    def __init__(self, queue, output_queue=None, start=True, **kwargs):
        super().__init__(**kwargs)
        self._queue: Queue = queue
        self._output_queue: Queue = (
            output_queue  # we can extend it to a list for different DB workers
        )
        if start:
            self.start()

    def _send_message_to_output_queue(self, message):
        if self._output_queue:
            self._output_queue.put(message)

    def run(self):
        while True:
            try:
                value = self._queue.get(timeout=50)  # blocking operation
            except Empty as exc:
                # is going to stop due to the fact is not values queued
                # timeout not to short because it could be just delays
                print(str(exc))
                break

            if value == "DONE":
                # self._send_message_to_output_queue("DONE")
                break

            yahoo_worker = YahooFinancePriceWorker(value)
            symbol_price = yahoo_worker.get_price()
            print(symbol_price)
            self._send_message_to_output_queue((value, symbol_price, datetime.utcnow()))
            time.sleep(random.random())
            # return symbol_price never return because the process finished
        print(f"{self} finished")


class YahooFinancePriceWorker:  # Thread
    BASE_URL = "https://finance.yahoo.com/quote/"

    def __init__(self, symbol, **kwargs):
        # super().__init__(**kwargs)
        self._symbol = symbol
        self._url = f"{YahooFinancePriceWorker.BASE_URL}{self._symbol}"
        # self.start()

    def get_price(self):
        time.sleep(30 * random.random())
        response = requests.get(self._url)
        if response.status_code != 200:
            return
        tree = html.fromstring(response.text)
        try:
            symbol_price_non_format = tree.xpath(
                '//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]'
            )[0].text
        except IndexError:
            print("index error")
            symbol_price_non_format = "0"

        symbol_price = float(symbol_price_non_format.replace(",", ""))

        return symbol_price
