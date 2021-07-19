from itertools import combinations_with_replacement, zip_longest, combinations

# This implementation uses a lot of memory when faced with a lot of numbers
def naive_grouper(inputs, n):
    num_groups = len(inputs) // n
    return [tuple(inputs[i * n : (i + 1) * n]) for i in range(num_groups)]


def better_grouper(inputs, n):
    # Creates a list of n references to the same iterator
    # [139949748267160, 139949748267160]
    iters = [iter(inputs)] * n
    # returns an iterator over pairs of corresponding elements of each iterator in iters
    return zip_longest(*iters, fillvalue=None)


# nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# print(list(better_grouper(nums, 4)))

bills = [20, 20, 20, 10, 10, 10, 10, 10, 5, 5, 1, 1, 1, 1, 1]


def split_money(money):
    # return [
    #     combination
    #     for i in range(
    #         len(money)
    #         for combination in combinations(money, i)
    #         if sum(combination) == 100
    #     )
    # ]
    result = []
    for i in range(len(money)):
        for combination in combinations(money, i):
            if sum(combination) == 100:
                result.append(combination)
    return set(result)


bills2 = [50, 20, 10, 5, 1]


def split_money2(money):
    results = []
    for n in range(1, 101):
        for combination in combinations_with_replacement(iterable=money, r=n):
            if sum(combination) == 100:
                results.append(combination)
    return results


print(split_money(bills))
print(split_money2(bills2))
