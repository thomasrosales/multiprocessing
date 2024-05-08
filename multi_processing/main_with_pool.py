from functools import partial
from multiprocessing import Pool, cpu_count

import time


def do_staff(y, additional_component, x):
    return x ** y + additional_component


power = 3
additional_component = 4
partial_function = partial(do_staff, power, additional_component)

if __name__ == '__main__':
    num_process = 4
    comparison_list = [1, 2, 3]
    start_time = time.time()

    print(f"CPUs available {cpu_count()}")

    cpus_available_for_process = max(1, cpu_count() - 1)

    with Pool(cpus_available_for_process) as processing_pool:
        # pool of processes we can use
        # define of number of processes available
        # https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool
        result = processing_pool.map(partial_function, comparison_list)  # function

    print(f"Everything took: {time.time() - start_time} seconds")
    print(result)
