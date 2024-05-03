from threading import Thread

import requests

from .helpers import extract_company_symbols


class WikiWorker:

    def __init__(self):
        super().__init__()
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    def get_list_of_companies(self):
        response = requests.get(self._url)
        if response.status_code != 200:
            return []

        yield from extract_company_symbols(response.text)
