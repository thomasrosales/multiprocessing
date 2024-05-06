import os
from multiprocessing import Queue
from queue import Empty
from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy.sql import text


class PostgresMasterScheduler(Thread):

    def __init__(self, queue, output_queue=None, start=True, **kwargs):
        super().__init__(**kwargs)
        self._queue: Queue = queue
        self._output_queue: Queue = output_queue
        if start:
            self.start()

    def run(self):
        while True:
            try:
                value = self._queue.get(timeout=50)
            except Empty as exc:
                # is going to stop due to the fact is not values queued
                # timeout not to short because it could be just delays
                print(str(exc))
                break

            if value == "DONE":
                break

            symbol, price, extracted_time = value
            postgres_worker = PostgresWorker(symbol, price, extracted_time)
            postgres_worker.insert_into_db()
        print(f"{self} finished")


class PostgresWorker:

    def __init__(self, symbol, price, extracted_time):
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time

        self._POSTGRES_USER_NAME = os.environ.get("PG_USER") or "postgres"
        self._POSTGRES_PASS = os.environ.get("PG_PASS") or "postgres"
        self._POSTGRES_HOST = os.environ.get("PG_HOST") or "localhost"
        self._POSTGRES_DB = os.environ.get("PG_DB") or "postgres"

        self._engine = create_engine(
            f"postgresql://{self._POSTGRES_USER_NAME}:{self._POSTGRES_PASS}@{self._POSTGRES_HOST}:5432/{self._POSTGRES_DB}"
        )

    def _create_insert_query(self):
        return """INSERT INTO prices (symbol, price, extracted_time) VALUES (:symbol, :price, :extracted_time)"""

    def insert_into_db(self):
        insert_query = self._create_insert_query()

        with self._engine.connect() as conn:
            conn.execute(
                text(insert_query),
                {
                    "symbol": self._symbol,
                    "price": self._price,
                    "extracted_time": str(self._extracted_time),
                },
            )
            conn.commit()  # commit the transaction
            # print(result)
