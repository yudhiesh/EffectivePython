import bisect as bs


def show_args_kwargs(*args, **kwargs):
    return print(f"Args = {args} Kwargs = {kwargs}")


one_dict = {"Address": "3212 Oakland Street", "Name": "Yudhiesh"}
two_dict = {"name": "max", "age": 12}


def merge_two_dicts(a, b):
    z = {**a, **b}
    return z


if __name__ == "__main__":
    ls = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
    print(bs.bisect(ls, 100))
    ls_sort = ls.sort()
    res = [i + 1 for i, num in enumerate(ls) if num < 100]
    print(res)
    assert res == len(ls)
