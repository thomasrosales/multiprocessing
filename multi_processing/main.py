from multiprocessing import Process, Queue
import time
from typing import List


def do_staff(value: List[int], i, number_of_process, q):
    max_number_to_check_to = 10 ** 8
    lower = int(i * max_number_to_check_to / number_of_process)
    upper = int((i + 1) * max_number_to_check_to / number_of_process)
    number_of_hits = 0
    for index in range(lower, upper):
        if index in value:
            number_of_hits += 1
    q.put((lower, upper, number_of_hits))


if __name__ == '__main__':
    num_process = 4
    comparison_list = [1, 2, 3]
    queue = Queue()
    process = []

    start_time = time.time()

    for i in range(num_process):
        p = Process(target=do_staff, args=(comparison_list, i, num_process, queue))
        process.append(p)

    for p in process:
        p.start()

    for p in process:
        p.join()

    queue.put("DONE")

    while True:
        v = queue.get()
        if v == "DONE":
            break
        l, u, hits = v
        print(f"lower {l}, upper {u}, and hits {hits}")

    print(f"Everything took: {time.time() - start_time} seconds")
