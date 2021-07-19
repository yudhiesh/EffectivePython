from threading import Thread, Lock

# Use Lock to Prevent Data Races in Threads
"""
When you have multiple threads accessing the same data structure it could lead
to data races where multiple of these threads have access to the same data
structure and perform mutable updates to the data structure. The Python
interpreter enforces fairness between all of the threads that are executing to
ensure they get roughly equal processing time. To do this Python suspends a
thread as it is running and resumes another thread in turn and you do not know
when this exactly happens, it could even happen when a thread is half way
through an atomic operation.
"""


class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        counter.increment(1)


how_many = 10 ** 5
counter = Counter()

threads = []
for i in range(5):
    thread = Thread(target=worker, args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f"Counter should be {expected}, got {found}")


class LockingCounter:
    def __init__(self) -> None:
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        # The lock protects the self.count from simultaneous accesses from
        # multiple threads. Only one thread will be able to access the lock at a
        # time.
        with self.lock:
            self.count += offset


counter = LockingCounter()
how_many = 10 ** 5

threads_locking = []
for i in range(5):
    thread = Thread(target=worker, args=(i, how_many, counter))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f"Counter should be {expected}, got {found}")
