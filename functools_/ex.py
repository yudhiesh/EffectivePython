from functools import partial, lru_cache, singledispatch, reduce
from time import time
import sys


def logger(log_level, message):
    print(f"[{log_level}]: {message}")


# logger("DEBUG", "message_one")
# logger("DEBUG", "message_two")
# logger("DEBUG", "message_three")

debug_logger = partial(logger, "DEBUG")

debug_logger("message_one")
debug_logger("message_two")
debug_logger("message_three")


# Least Recently Used
# It saves the result of last executed function in memory and when it has to
# again execute the function it will first check the cache and if it is found
# it will return the result otherwise it ill go on to execute the function
# Speeds the code up a lot!
@lru_cache(maxsize=128)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def fibo(n):
    if n <= 1:
        return n
    else:
        return fibo(n - 1) + fibo(n - 2)


def sum_of_fibo(nterms, fun):
    start = time()
    result = 0
    for i in range(nterms):
        result += fun(i)
    print(f"Total Sum {result} , Total time taken {time() - start} sec")


@singledispatch
def double_the_value(value):
    raise Exception(f"Type {type(value)} not supported")


# Overload the method
# This will be called when the argument is an int
@double_the_value.register(int)
def _(value):
    return value * 2


@double_the_value.register(list)
@double_the_value.register(tuple)
def _(value):
    return [v * 2 for v in value]


@double_the_value.register(dict)
def _(value):
    return {k: v * 2 for k, v in value.items()}


l = [10, 20, 20, 100, 230, 230]

if __name__ == "__main__":
    print(reduce(lambda x, y: x + y, l))
    print(reduce(lambda x, y: x + y, l, 100))
    print(reduce(max, l))
    print(reduce(min, l, sys.maxsize))
    print(reduce(min, l))
    # print(double_the_value(5))
    # print(double_the_value((5, 10)))
    # print(double_the_value([2, 3, 4, 5, 566]))
    # double_the_value("Hello World")
    # sum_of_fibo(30, fib)
    # sum_of_fibo(30, fibo)
