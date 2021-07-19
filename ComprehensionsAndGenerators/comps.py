import math
from time import time
from functools import wraps
from collections.abc import Iterator
from typing import Iterable

# Avoid More Than Two Control Subexpressions in Comprehensions

# Flattening a list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [value for row in matrix for value in row]
print(flat)

# Square each value in a multidimensional array
squared = [[value ** 2 for value in row] for row in matrix]
print(squared)

# Filter a list of numbers to only have even numbers > 4
a = [i for i in range(10)]
b = [x for x in a if x > 4 and x % 2 == 0]
print(b)

# Filter a matrix so the only cells remaining are those divisible by 3 in rows
# that sum to 10 or higher
filtered = [
    [value for value in row if value % 3 == 0] for row in matrix if sum(row) >= 10
]
print(filtered)

# NOTE: Avoid using more than two control subexpressions in a comprehensions

# Avoid Repeated Work in Comprehensions by Using Assignment Expressions
"""
For example, say that I am writing a program to manage orders for a company. As
new orders come in I need to be able to tell whether the order can be fullfilled
i.e. I need to verify that a request is sufficiently in stock and above the min
threshold for shipping(in batches of 8)
"""

stock = {"nails": 125, "screws": 35, "wingnuts": 8, "washers": 24}
order = ["screws", "wingnuts", "clips"]


def get_batches(count, size):
    return count // size


result = {}
batch_size = 8
for name in order:
    count = stock.get(name, 0)
    batches = get_batches(count, batch_size)
    if batches:
        result[name] = batches
print(result)


found = {
    name: get_batches(stock.get(name, 0), batch_size)
    for name in order
    if get_batches(stock.get(name, 0), batch_size)
}


def measure(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time() * 1000)) - start
            print(
                f"Total execution time: {end_ if end_ > 0 else 0 }ms for {func.__name__}()"
            )

    return _time_it


@measure
def a():
    return {
        name: get_batches(stock.get(name, 0), batch_size)
        for name in order
        if get_batches(stock.get(name, 0), batch_size)
    }


# The assignment expression aka the walrus operator allows me to look up the
# value for each order key in the stock dictionary a single time, call
# get_batches() once and then store the corresponding value in the batches
# variable


@measure
def b():
    return {
        name: batches
        for name in order
        if (batches := get_batches(stock.get(name, 0), batch_size))
    }


@measure
def c():
    # Make sure the assignment operator is created in the conditional part of a
    # comprehension
    return {name: tenth for name, count in stock.items() if (tenth := count // 10)}


if __name__ == "__main__":
    a()
    b()
    print(c())

# Consider Gerenators Instead of Returning Lists
# For example, say that I want to find the index of every word in a string


def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == " ":
            result.append(index + 1)
    return result


address = "Four score and seven years ago..."
result = index_words(address)
print(result)


def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == " ":
            yield index + 1


result_iter = list(index_words_iter(address))
print(result_iter)

# Be Defensive When Iterating Over Arguments
"""
For example, say that I want to analyze tourism numbers for the Texas. The
dataset is the number of visitors to each city(in millions per year). I'd like
to figure out what percentage of overall tourism each city receives.
"""


def normalize(numbers):
    total = sum(numbers)
    result = []
    for num in numbers:
        percent = 100 * (num / total)
        result.append(percent)
    return result


visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)  # [11.538461538461538, 26.923076923076923, 61.53846153846154]
assert sum(percentages) == 100.0

# Reading the inputs from a file instead of a list of numbers
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)


"""
Calling this function on the input path of the numbers will result in an empty
[] being returned, this happens because an iterator produces its results only
a single time, if the iterator or generator has already raised a StopIteration
exception you won't get any results the second time around.
You won't get any errors when you iterate over an already exhausted iterator.
A better way to solve this is to provide a new container class that implements
the iterator protocol.
All you have to do is implement the __iter__ method as a generator.
"""


class ReadVisits:
    def __init__(self, data_path: str) -> None:
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


"""
This works because the sum method in normalize calls ReadVisits.__iter__ to
allocate a new iterator object.
"""


def normalize_defensive(numbers):
    # Test if an iterator is passed in and throw an error because the protocol
    # states that when an iterator is passed to the iter built-in function, iter
    # returns the iterator itself and if it is a container type a new iterator
    # object is returned each time.
    if isinstance(numbers, Iterator):
        raise TypeError("Must supply a container")
    total = sum(numbers)
    result = []
    for number in numbers:
        percent = 100 * (number / total)
        result.append(percent)
    return result


# visits = ReadVisits(data_path="test.txt")
# percentages_ = normalize_defensive(visits)


# Compose Multiple Generators with yield from

"""
Say that I have a graphical program that uses generators to animate the movement
of images onscreen. To get the visual effect I'm looking for, I need the images
to move quickly at first, pause temporarily, and then continue moving at a
slower pace.
"""


def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({args!r}, {kwargs!r}) -> {result!r}")
        return result

    return wrapper


@trace
def move(period: int, speed: float):
    for _ in range(period):
        yield speed


@trace
def pause(delay):
    for _ in range(delay):
        yield 0


@trace
def animate():
    for delta in move(4, 5.0):
        yield delta
    for delta in pause(3):
        yield delta
    for delta in move(2, 3.0):
        yield delta


@trace
def render(delta: float):
    print(f"Delta: {delta:.1f}")


@trace
def run(func):
    for delta in func():
        render(delta)


# run(animate)

# Problem with this code is the repetitive nature of the yield statements
# from the generators which can be solved by using yield from
# Under the hood python handles all the nested for loops and yield expression
# boilerplate.


def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)


run(animate_composed)


# Avoid Injecting Data into Generators with send
"""
yield expressions provide generator functions with a simple way to produce an
iterable series of output values. This is a unidirectional flow of data whereas
to enable bidirectional communication we would have to use *send*.
For example, here I am writing a program to transmit signals using software
defined radio. 
"""


def wave(amplitude, steps):
    """
    Generate an approximation of a sine wave with a given number of points
    """
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        yield output


def transmit(output):
    if output is None:
        print(f"Output is None")

    else:
        print(f"Output: {output:>5.1f}")


def run_(it):
    for output in it:
        transmit(output)


run_(wave(3.0, 8))

# This works fine for producing basic waveforms but it can't be used to
# constantly vary the amplitude of the wave based on a separate input, for that
# I will need a way to modulate the amplitude on each iteration of the generator

# Normally when iterating over a generator the value of the yield expression is
# None


def my_generator():
    received = yield 1
    print(f"received = {received}")


# it = iter(my_generator())
# output = next(it)  # Get first generator output
# print(f"Output = {output}")
# try:
#     next(it)  # Run generator until it exits
# except StopIteration:
#     pass

it_ = iter(my_generator())
output_send = it_.send(None)  # Get first generator output
print(f"output = {output_send}")
try:
    it_.send("Hello!")  # Send value into the generator
except StopIteration:
    pass

"""
When calling the send() instead of iterating the generator with a for loop or
with the next(), the supplied parameter becomes the value of the yield
statement. However, when the generator first starts, a yield expression has not
been encountered yet, sot the only valid value for calling send initially is
None
"""


def wave_modulating(steps):
    step_size = 2 * math.pi / steps
    amplitude = yield  # Receive initial amplitude
    print(f"Amplitude outside for loop: {amplitude}")
    for step in range(steps):
        print(f"Step: {step}")
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        amplitude = yield output  # Receive next amplitude
        print(f"Amplitude inside for loop: {amplitude}")


def run_modulating(it):
    amplitudes = [None, 7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    for amplitude in amplitudes:
        output = it.send(amplitude)
        transmit(output)


run_modulating(wave_modulating(12))


def wave_cascading(amplitude_it, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        amplitude = next(amplitude_it)
        output = amplitude * fraction
        yield output  # Receive next amplitude


def complex_wave_cascading(amplitude_it):
    yield from wave_cascading(amplitude_it, 3)
    yield from wave_cascading(amplitude_it, 4)
    yield from wave_cascading(amplitude_it, 5)


def run_cascading():
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    it = complex_wave_cascading(iter(amplitudes))
    for amplitude in amplitudes:
        output = next(it)
        transmit(output)


run_cascading()


