import itertools

# Naive way
def even():
    num = 0
    while True:
        yield num
        num += 2


def odd():
    num = 1
    while True:
        yield num
        num += 2


# e = even()
# print(list(next(e) for _ in range(100)))
# o = odd()
# print(list(next(o) for _ in range(100)))

# Itertools way

even_counter = itertools.count(0, step=2)
odd_counter = itertools.count(1, step=2)
neg_count = itertools.count(-1, step=-0.5)
# print(list(next(even_counter) for _ in range(100)))
# print(list(next(odd_counter) for _ in range(100)))
# print(list(next(neg_count) for _ in range(100)))
# print(list(zip(itertools.count(), ["a", "b", "v", "e", "t"])))


def fibs():
    x, y = 0, 1
    while True:
        yield x
        x, y = y, x + y


f = fibs()
# for _ in range(100_000):
#     print(next(f))

# print(list(itertools.accumulate([1, 2, 3, 4, 5], lambda x, y: (x + y) / 2)))
ranks = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
suits = ["H", "D", "C", "S"]

# cards = ((rank, suit) for rank in ranks for suit in suits)
# print(list(cards))
cards = itertools.product(ranks, suits)

# Chains any amount of iterable items
# print(list(itertools.chain(ranks, suits, ranks, suits)))


def cut(deck, n):
    """Return an iterator over a deck of cards cut at index `n`."""
    deck1, deck2 = itertools.tee(deck, 2)
    top = itertools.islice(deck1, n)
    bottom = itertools.islice(deck2, n, None)
    return itertools.chain(bottom, top)


cards = cut(cards, 26)


def deal(deck, num_hands, hand_size):
    iters = [iter(deck)] * hand_size
    return tuple(zip(*(tuple(itertools.islice(itr, num_hands)) for itr in iters)))


p1_hand, p2_hand, p3_hand = deal(cards, num_hands=3, hand_size=5)
# print(p1_hand)
# print(p2_hand)
# print(p3_hand)
# print(len(tuple(cards)))

print(list(itertools.chain.from_iterable([[1, 2, 3], [2, 3, 4]])))
