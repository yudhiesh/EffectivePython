# Creating an iterator from scratch


class Repeater:
    def __init__(self, value):
        self.value = value

    def __iter__(self):
        return RepeaterIterator(self)


# Link the RepeaterIterator to each of the Repeater instances
# With this we can hold on to the source object that is being iterated over
# in __next__ we reach back into the source Repeater instance, return the value associated with it
class RepeaterIterator:
    def __init__(self, source):
        self.source = source

    def __next__(self):
        return self.source.value


class RepeaterBetter:
    def __init__(self, value):
        self.value = value

    def __iter__(self):
        return self

    def __next__(self):
        return self.value


class BoundedRepeater:
    def __init__(self, value, max_repeats):
        self.value = value
        self.max_repeats = max_repeats
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.max_repeats:
            raise StopIteration
        self.count += 1
        return self.value


# repeater = Repeater("Hello")
# repeater = RepeaterBetter("Hi")
repeater = BoundedRepeater("Hi", 4)
# Calling iter() is similar to calling __iter__()
iterator = iter(repeater)
# Calling next() is similar to calling __next__()
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))
# Both are the same ways of iterating over the iterator
# iterator = repeater.__iter__()
# while True:
#     item = iterator.__next__()
#     print(item)
