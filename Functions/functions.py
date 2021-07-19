import json
from typing import List, Optional, Set, Tuple
from functools import wraps
from time import sleep
from datetime import datetime


# Prefer raising exceptions over returning None
def careful_divide(a: float, b: float) -> float:
    """
    Divides a by b
    Raises:
        ValueError: When the inputs cannot be divided
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError("Invalid Inputs")


x, y = 5, 0
try:
    result = careful_divide(x, y)
except ValueError:
    print("Invalid inputs")
else:
    print("Result is %.1f" % result)

# Know How Closures Interact with Variable Scope
"""
Say that I want to sort a list of numbers but prioritize one group of numbers to come first.
"""


# Although the function works debugging the nonlocal issues is a difficult issue
# and it is better to use a class to perform this action
def sort_priority(values: List[int], group: Set):
    found: bool = False

    def helper(value: int):
        nonlocal found
        if value in group:
            found = True
            return (0, value)
        return (1, value)

    values.sort(key=helper)
    return found


class Sorter(object):
    def __init__(self, group: Set) -> None:
        self.group = group
        self.found: bool = False

    def __call__(self, value: int) -> Tuple[int, int]:
        if value in self.group:
            self.found = True
            return (0, value)
        return (1, value)


numbers: List[int] = [8, 3, 1, 2, 5, 4, 7, 6]
group_: Set = {2, 3, 5, 7}

# status = sort_priority(values=numbers, group=group_)
# print(numbers)
# print(status)

sorter = Sorter(group_)
print(numbers)
numbers.sort(key=sorter)
print(numbers)
assert sorter.found

# Reduce Visual Noise with Variable Positional Arguments
"""
Issues with accepting a variable number of positional arguments:
1. These optional positional arguments are turned into a tuple before they are
passed to a function. If a caller of a function uses the * operator on a
generator it will be iterated until it's exhausted. The resulting tuple includes
every value from the generator which could consume a lot of memory and crash the
program
2. You can't add positional arguments to a function in the future without
migrating every caller.
"""


def log(message: str, *values):
    if not values:
        print(message)
    else:
        values_str = ", ".join(str(x) for x in values)
        print(f"{message}: {values_str}")


log("My numbers are", [1, 2])  # New with *args OK
log("Hi there")  # New message only OK
log("Hi there", 7, 33)  # Old usage breaks

# Provide Optional Behavior with Keyword Arguments


def remainder(number: int, divisor: int) -> int:
    return number % divisor


my_kwargs = {"number": 20, "divisor": 7}

assert remainder(**my_kwargs) == 6


# If you would like a function to receive any named keyword argument you can use
# the **kwargs catch all parameter to collect those arguments into a dict that
# you can process
def print_parameters(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} = {value}")


print_parameters(alpha=0.5, beta=9, gamma=4)

# Use None and Docstrings to Specify Dynamic Default Arguments
"""
Somtimes you need a non-static type as a keyword arguments default value. 
For example, say I want to print logging messages that are marked with the time
of the logged event. 
"""


def log(message: str, when=None):
    """
    Log a message with a timestamp
    Args:
        message: Message to print
        when: datetime of when the message occurred
            Defaults to the present time
    """
    if not when:
        when = datetime.now()
    print(f"{when} : {message}")


log("Hi there!")
sleep(1)
log("Hello how are you?")

"""
Using None for default values is especially important when the arguments are
mutable. 
For example, say that I want to load a value encoded as JSON data; if decoding
fails, I want an empty dictionary to be returned by default.
"""


def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default


foo = decode("bad data")
foo["stuff"] = 5
bar = decode("also bad")
bar["meep"] = 1
print("Foo: ", foo)
print("Bar: ", bar)
# The problem here is that the dictionary specified for default will be shared
# by all calls to decode because default argument values are evaluated only
# once(at module load time)


def decode_correct(data, default=None):
    """
    Load JSON data from a string

    Args:
        data: JSON data to decode
        default: Value to return if decoding fails.
            Defaults to an empty dictionary
    """
    try:
        return json.loads(data)
    except ValueError:
        if not default:
            default = {}
    return default


foo_ = decode_correct("bad data")
foo_["stuff"] = 5
bar_ = decode_correct("also bad")
bar_["meep"] = 1
print("Foo: ", foo_)
print("Bar: ", bar_)
empty = decode_correct("")
print("Empty: ", empty)


def log_typed(message: str, when: Optional[datetime] = None) -> None:
    """Log a message with a timestamp

    Args:
        message: Message to print
        when: datetime of the message
            Defaults to the present time
    """
    if not when:
        when = datetime.now()
    print(f"{when}: {message}")


log_typed("Hi there! How are you?")
sleep(1)
log_typed("I am fine thanks!")

# Enforce Clarity with Keyword-Only and Positional-Only Arguments


def safe_division(
    number, divisor, *, ignore_overflow=False, ignore_zero_division=False
):
    # The * in the argument list indicates the end of the positional arguments
    # and the start of the beginning of the keyword-only arguments
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float("inf")
        else:
            raise


result = safe_division(1.0, 10 ** 500, ignore_overflow=True)

# Define Function Decorators with functools.wraps
"""
A decorator has the ability to run additional code before and after each call to
a function it wraps. 
For example, say that I want to print the arguments and return the value of a
function call.
"""


def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({args!r}, {kwargs!r}) -> {result!r}")
        return result

    return wrapper


@trace
def fibonacci(n: int) -> int:
    """Return the n-th Fibonacci number

    Args:
        n: n-th Fibonacci number
    """
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


help(fibonacci)
