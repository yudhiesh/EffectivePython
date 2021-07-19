import time
from queue import Queue
from collections import deque
from threading import Lock, Thread

# Use Queue to Coordinate Work Between Threads


def download(item):
    ...


def resize(item):
    ...


def upload(item):
    ...


class MyQueue:
    def __init__(self) -> None:
        self.items = deque()
        self.lock = Lock()

    # Producer adds new images to the end of the deque
    def put(self, item):
        with self.lock:
            self.items.append(item)

    # Consumer removes images from the front of the deque of pending items
    def get(self):
        with self.lock:
            return self.items.popleft()


class Worker(Thread):
    def __init__(self, func, in_queue: MyQueue, out_queue: MyQueue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                time.sleep(0.01)
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


# download_queue = MyQueue()
# resize_queue = MyQueue()
# upload_queue = MyQueue()
# done_queue = MyQueue()

# threads = [
#     Worker(download, download_queue, resize_queue),
#     Worker(resize, resize_queue, upload_queue),
#     Worker(upload, upload_queue, done_queue),
# ]

# for thread in threads:
#     thread.start()

# for _ in range(1000):
#     download_queue.put(object())

# while len(done_queue.items) < 1000:
#     ...

# processed = len(done_queue.items)
# polled = sum(thread.polled_count for thread in threads)
# # Processed 1000 items after polling 3009 times
# print(f"Processed {processed} items after polling {polled} times")

"""
When the workers vary in respective speed, an earlier phase can prevent progress
in later phases, backing up the pipeline. This causes later phases to starve and
constantly check their input queues for new work in a tight loop. Worker threads
end up wasting CPU time doing nothing useful.

A backup in the pipeline can cause the program to crash arbitrarily. If the
first phase makes rapid progress but the second phase makes slow progress, then
the queue connecting the two of them will constantly increase in size. The
second phase won't be able to keep up. Given enough time and memory the program
will eventually run out of memory.
"""

my_queue = Queue()


def consumer():
    print("Consumer waiting")
    my_queue.get()
    print("Consumer done")


# Even though the thread is running first, it won't finish until an item is put
# on the Queue instance and the get method has something to return
# thread = Thread(target=consumer)
# thread.start()
# print("Producer putting")
# my_queue.put(object())
# print("Producer done")
# thread.join()

"""
Consumer waiting
Producer putting
Producer done
Consumer done
"""


class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue) -> None:
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()

threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

download_queue.close()
download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), "items finished")

for thread in threads:
    thread.join()


def start_threads(count, *args):
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads


def stop_threads(closable_queue, threads):
    for _ in threads:
        closable_queue.close()
    closable_queue.join()
    for thread in threads:
        thread.join()


download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()

download_threads = start_threads(3, download, download_queue, resize_queue)
resize_threads = start_threads(4, resize, resize_queue, upload_queue)
upload_threads = start_threads(5, upload, upload_queue, done_queue)

for _ in range(1000):
    download_queue.put(object())

stop_threads(download_queue, download_threads)
stop_threads(resize_queue, resize_threads)
stop_threads(upload_queue, upload_threads)

print(done_queue.qsize(), "items finished")
