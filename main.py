import time

from multiprocessing import Queue

from core.executor import PipelineExecutor
from workers.postgres import PostgresMasterScheduler
from workers.sleeps import SleepyWorker
from workers.squared_sum import SquaredSumWorker
from workers.wiki import WikiWorker
from workers.yahoo_finance import YahooFinancePriceWorker, YahooFinancePriceScheduler


def main_1():
    calc_start_time = time.time()
    current_threads = []

    for index in range(5):
        args = (index + 1) * 1000000
        # t = threading.Thread(target=calculate_sum_squares, args=(args,))  # daemon=True  https://docs.python.org/3/library/threading.html#threading.Thread.daemon
        # t.start()
        # current_threads.append(t)
        # calculate_sum_squares((index + 1) * 1000000)
        worker_thread = SquaredSumWorker(args)
        current_threads.append(worker_thread)

    for i in range(len(current_threads)):
        current_threads[i].join()  # Wait until the thread terminates.

    print(f"Calculating time of square took: {time.time() - calc_start_time}")

    calc_start_time = time.time()
    current_threads = []

    for index in range(1, 6):
        # t = threading.Thread(target=sleep_a_little, args=(index,))
        # t.start()
        worker_thread = SleepyWorker(index)
        current_threads.append(worker_thread)
        # sleep_a_little(index)

    for i in range(len(current_threads)):
        current_threads[i].join()  # Wait until the thread terminates.

    print(f"Calculating time of square took: {time.time() - calc_start_time}")


def main_2():
    calc_start_time = time.time()
    current_threads = []

    wiki = WikiWorker()
    for company in wiki.get_list_of_companies():
        yahoo_worker = YahooFinancePriceWorker(company)
        current_threads.append(yahoo_worker)

    for i in range(len(current_threads)):
        current_threads[i].join()

    print(f"Calculating time of square took: {time.time() - calc_start_time}")


def main_3():
    symbol_queue = Queue()

    calc_start_time = time.time()

    wiki = WikiWorker()
    yahoo_master_thread_scheduler = YahooFinancePriceScheduler(symbol_queue)

    for company in wiki.get_list_of_companies():
        symbol_queue.put(company)
    symbol_queue.put("DONE")

    yahoo_master_thread_scheduler.join()

    print(f"Calculating time of square took: {time.time() - calc_start_time}")


def main_4():
    symbol_queue = Queue()
    postgres_queue = Queue()

    calc_start_time = time.time()

    wiki = WikiWorker()
    yahoo_finance_price_scheduler_threads = []
    num_yahoo_finance_price_worker = 4

    for i in range(num_yahoo_finance_price_worker):
        yahoo_master_thread_scheduler = YahooFinancePriceScheduler(symbol_queue, output_queue=postgres_queue)
        yahoo_finance_price_scheduler_threads.append(yahoo_master_thread_scheduler)

    postgres_scheduler_threads = []
    num_postgres_worker = 2
    for i in range(num_postgres_worker):
        postgres_thread_scheduler = PostgresMasterScheduler(queue=postgres_queue)
        postgres_scheduler_threads.append(postgres_thread_scheduler)

    for company in wiki.get_list_of_companies():
        symbol_queue.put(company)
    [symbol_queue.put("DONE") for _ in range(num_yahoo_finance_price_worker)]

    for i in range(len(yahoo_finance_price_scheduler_threads)):
        yahoo_finance_price_scheduler_threads[i].join()

    for i in range(len(postgres_scheduler_threads)):
        postgres_scheduler_threads[i].join()

    print(f"Calculating time of square took: {time.time() - calc_start_time}")


def main_5():
    calc_start_time = time.time()
    executor = PipelineExecutor("pipelines/wiki_pipeline.yaml")
    executor.start()
    print(f"Calculating time of square took: {time.time() - calc_start_time}")


if __name__ == "__main__":
    main_5()
