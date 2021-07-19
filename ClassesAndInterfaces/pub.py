from collections.abc import Sequence

# Prefer Public Attributes Over Private Ones


class MyObject:
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field


foo = MyObject()
assert foo.public_field == 5
assert foo.get_private_field() == 10
# foo.__private_field will throw an exception


class MyOtherObject:
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field


bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71


class MyParentObject:
    def __init__(self):
        self.__private_field = 71


class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field


baz = MyChildObject()
# baz.get_private_field() will throw an exception error
assert baz._MyParentObject__private_field == 71
print(baz.__dict__)


# Inherit from collections.abs for Custom Container Types


class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts[item] = counts.get(item, 0) + 1
        return counts


foo = FrequencyList(["a", "b", "c", "d", "e", "a", "b", "e", "f"])
print(f"Length is {len(foo)}")
foo.pop()
print(f"After pop {repr(foo)}")
print(f"Frequency: {foo.frequency()}")


class BinaryNode:
    def __init__(self, value, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right


class IndexableNode(BinaryNode):
    def _traverse(self):
        if self.left is not None:
            yield from self.left._traverse()
        yield self
        if self.right is not None:
            yield from self.right._traverse()

    def __getitem__(self, index):
        for i, item in enumerate(self._traverse()):
            if i == index:
                return item.value
        raise IndexError(f"Index {index} is out of range!")


tree = IndexableNode(
    10,
    left=IndexableNode(5, left=IndexableNode(2), right=IndexableNode(6)),
    right=IndexableNode(11),
)

print("LRR is", tree.left.right.value)
print("Index 0 is", tree[0])
print("Index 1 is", tree[1])
print("Tree list: ", list(tree))

# implementing __getitem__ is not sufficient to provide all the sequence
# semantincs that you'd expect from a list instance
# len(tree) throws an error


class SequenceNode(IndexableNode):
    def __len__(self):
        for count, _ in enumerate(self._traverse(), 1):
            pass
        return count


# To solve this subclass from the abstract base classes in collections


class BetterNode(SequenceNode, Sequence):
    pass


tree_better = BetterNode(
    10,
    left=BetterNode(5, left=BetterNode(2), right=BetterNode(6)),
    right=BetterNode(11, left=BetterNode(10, left=BetterNode(2), right=BetterNode(2))),
)

mro_str = "\n".join(repr(cls) for cls in BetterNode.mro())
print(mro_str)
print("Tree Better: ", list(tree_better))
print(len(tree_better))
print("Index of 6 is", tree_better.index(6))
print("Index of 2 is", tree_better.index(2))
