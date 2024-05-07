from threading import Thread, Lock

counter = 0  # Global Access -> Generates raise conditions

lock = Lock()


def increment():
    global counter
    for _ in range(10 ** 6):
        lock.acquire()
        counter += 1
        lock.release()


def increment_with_context_manager():
    global counter
    for _ in range(10 ** 6):
        with lock:
            counter += 1


threads = []

for i in range(4):
    t = Thread(target=increment)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print(f"Counter value: {counter}")
