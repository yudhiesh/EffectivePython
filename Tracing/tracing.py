import functools


def tracefunc(func):
    """Decorates a function to show its trace."""

    @functools.wraps(func)
    def tracefunc_closure(*args, **kwargs):
        """The closure."""
        result = func(*args, **kwargs)
        print(f"{func.__name__}(args={args}, kwargs={kwargs}) => {result}")
        return result

    return

@tracefunc
def show_args_and_kwargs(*args, **kwargs):
    return


if __name__ == "__main__":

    show_args_and_kwargs(10)
    show_args_and_kwargs(color="Red")
    show_args_and_kwargs(10, 200, color="Blue", type="Dog")
