import time
import select
import socket
from threading import Thread

# Use Threads for Blocking I/O, Avoid for Parallelism

"""
Standard implementation of Python is CPython which runs a Python program in 2
steps:
1. Parse and compile the source text into bytecode/wordcode
2. Run the bytecode using a stack-based interpreter
The state of the bytecode interpreter has must be maintained and coherent while
the program executes. Coherence is enforced using the Global Interpreter
Lock(GIL)
GIL is a mutex that prevents CPython from being affected by preemptive
multithreading, where one thread takes control of another thread by interrupting
another thread, this could corrupt the interpreter state if it comes at an
unexpected time.
Downside of the GIL is that only a single thread to ever be able to make
progress at a time.
"""


def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


numbers = [1212543, 2341242, 132221, 8742243]

start = time.time()

for number in numbers:
    list(factorize(number))

end = time.time()
delta = end - start
print(f"Took {delta:.3f} seconds")

# Using multiple threads would make sense in other languages as I could take
# advantage of all the CPU cores of my computer.


class FactorizeThread(Thread):
    def __init__(self, number) -> None:
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


start = time.time()

threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f"Took {delta:.3f} seconds")

# Surprisingly this takes about the same amount of time even with a thread per
# number at least it should be 4x faster or 2x faster
# This demonstrates the effects of the GIL

"""
Why does Python support threads at all?
1. Multiple threads make it easy to seem like it's doing multiple things at the
same time. With threads, Python makes it seem like your threads are running in
parallel which is easier than you having to do it yourself
2. Deal with blocking I/O

A Python program uses system calls to ask the computer's OS to interact with the
external environment on its behalf. Blocking I/O includes read/write files,
network requests, communicating with devices etc.

For example, say that I want to send a signal to a remote-control helicopter
through a serial port. I'll use a slow system call(select) as a proxy for this
activity. This function asks the OS to block for 1 seconds and then returns
control to my program, which is similar to what would happen when using a
synchronous.
"""


def slow_system_call():
    select.select([socket.socket()], [], [], 1)


start = time.time()
threads = []
for _ in range(5):
    thread = Thread(target=slow_system_call)
    thread.start()
    threads.append(thread)


def compute_helicopter_location(index):
    return index ** 100


for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f"Took : {delta:.3f} seconds")

# This code runs faster and is running in parallel as it is a system call and
# Python threads release the GIL just before they make system calls, and then
# reacquire the GIL as soon as the system calls are done.
