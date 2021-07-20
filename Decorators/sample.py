import time
from functools import wraps


def log(func_in=None, *, show_time=True, show_name=True):
    def stopwatch(f):
        @wraps(f)
        def func(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            log_text = ""
            if show_name:
                log_text = f"{log_text}name: {f.__name__}"
            if show_time:
                log_text = f"{log_text}\ntime: {time.time() - start}"
            print(log_text)
            return result

        return func

    if not func_in:
        return stopwatch
    else:
        return stopwatch(func_in)


@log()
def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


if __name__ == "__main__":
    print(fibonacci(100))

