from multiprocessing import Queue
from threading import Thread

import requests

from .helpers import extract_company_symbols


class WikiWorkerMaster(Thread):

    def __init__(self, *args, output_queue=None, start=True, **kwargs):
        super().__init__(**kwargs)
        self._output_queue: Queue = (
            output_queue  # we can extend it to a list for different DB workers
        )
        if start:
            self.start()

    def run(self):
        while True:
            wiki_worker = WikiWorker()
            for company in wiki_worker.get_list_of_companies():
                self._output_queue.put(company)
            return


class WikiWorker:

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    def get_list_of_companies(self):
        response = requests.get(self._url)
        if response.status_code != 200:
            return []

        yield from extract_company_symbols(response.text)
