from collections import defaultdict
from typing import DefaultDict, Dict, List, NamedTuple, Tuple

# Compose Classes Instead of Nesting Many Levels of Built-in Types
# NOTE: For example, say I want to record the grades of students whose names
# aren't known in advance. I can define a class to store the names in a
# dictionary.


class SimplestGradeBook:
    def __init__(self) -> None:
        self._grades: Dict[str, List[int]] = {}

    def add_student(self, name: str) -> None:
        self._grades[name] = []

    def report_grade(self, name: str, score: int) -> None:
        self._grades[name].append(score)

    def average_grade(self, name: str):
        grades = self._grades[name]
        return round(sum(grades) / len(grades), 2)


book = SimplestGradeBook()
book.add_student("Isaac Newton")
book.report_grade("Isaac Newton", 90)
book.report_grade("Isaac Newton", 85)
book.report_grade("Isaac Newton", 88)
book.add_student("Yudhiesh Ravindranath")
book.report_grade("Yudhiesh Ravindranath", 88)
book.report_grade("Yudhiesh Ravindranath", 75)
book.report_grade("Yudhiesh Ravindranath", 70)


# You cannot specify default arguments when using namedtuple
# The attribute values of namedtuple instances are still accessible using
# numerical indexes and iteration.
# If you are not in control of your namedtuple instances then it is better to
# use a new class


class Grade(NamedTuple):
    score: int
    weight: float


class Subject:
    def __init__(self) -> None:
        self._grades: List[Grade] = []

    def report_grade(self, score: int, weight: float) -> None:
        self._grades.append(Grade(score, weight))

    def average_grade(self) -> float:
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student:
    def __init__(self) -> None:
        self._subjects: DefaultDict[str, Subject] = defaultdict(Subject)

    def get_subject(self, name: str):
        return self._subjects[name]

    def average_grade(self) -> float:
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return round(total / count, 2)


class GradeBook:
    def __init__(self) -> None:
        self._students: DefaultDict[str, Student] = defaultdict(Student)

    def get_student(self, name) -> Student:
        return self._students[name]


grade_book = GradeBook()
albert = grade_book.get_student("Albert Einstein")
math = albert.get_subject("Math")
math.report_grade(75, 0.05)
math.report_grade(65, 0.15)
math.report_grade(70, 0.80)
gym = albert.get_subject("Gym")
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)
print(albert.average_grade())

# Accept Functions Instead of Classes for Simple Interfaces

names = ["Socrates", "Archimedes", "Plato", "Aristotle"]
print(names)
names.sort(key=len)  # pass in the built-in function len
print(names)


def log_missing() -> int:
    print("Key added")
    return 0


current = {"green": 12, "blue": 3}
increments = [("red", 5), ("blue", 17), ("orange", 9)]
# call log_missing everytime a missing key is accessed
result = defaultdict(log_missing, current)
print(f"Before: {dict(result)}")
for key, amount in increments:
    result[key] += amount
print(f"After: {dict(result)}")

# Supplying functions like log_missing makes APIs easy to build and test because
# it separates side effects from deterministic behavior

Zero = type(0)

# Increment the count whenever there is a missing key
def increment_with_report(
    current: Dict[str, int], increments: List[Tuple[str, int]]
) -> Tuple[DefaultDict[str, int], int]:
    added_count: int = 0

    # Using a closure is fine but difficult to read
    def missing() -> Zero:
        nonlocal added_count
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount
    return result, added_count


result, count = increment_with_report(current, increments)
assert count == 2


class CountMissing:
    def __init__(self) -> None:
        self.added: int = 0

    def missing(self) -> Zero:
        self.added += 1
        return 0


# Although better than using a closure this class in isolation its still not
# obvious what the purpose of the CountMissing class is
# Who constructs the class? Who calls the missing method?
# Until you see the usage with defaultdict, the class is a mystery

counter = CountMissing()
result = defaultdict(counter.missing, current)
for key, amount in increments:
    result[key] += amount
assert counter.added == 2


class BetterCountMissing:
    def __init__(self) -> None:
        self.added: int = 0

    def __call__(self):
        self.added += 1
        return 0


counter = BetterCountMissing()
assert callable(counter)
result = defaultdict(counter, current)
for key, amount in increments:
    result[key] += amount
assert counter.added == 2


# Initialize Parent Classes with super

"""
super() ensures that common superclasses are only run once
"""


class MyBaseClass:
    def __init__(self, value):
        self.value = value


class TimesSevenCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 7


class PlusNineCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value += 9


class GoodWay(PlusNineCorrect, TimesSevenCorrect):
    def __init__(self, value):
        super().__init__(value)


foo = GoodWay(5)
assert foo.value == 44

# Method Resolution Order(MRO)
mro_str = "\n".join(repr(cls) for cls in GoodWay.mro())
print(mro_str)

# Order of the class initialization actually goes backwards from what is
# expected, GoodWay -> PlusNineCorrect -> TimesSevenCorrect -> MyBaseClass where
# each .__init__() is called within the classes. Once at the top of the diamond
# the work is done in the reverse order MyBaseClass sets value to 5,
# TimesSevenCorrect multiplies the value with 7 = 35, PlusNineCorrect adds 9 to
# the value = 44
"""
<class '__main__.GoodWay'>
<class '__main__.PlusNineCorrect'>
<class '__main__.TimesSevenCorrect'>
<class '__main__.MyBaseClass'>
<class 'object'>
"""


# The super function can also be called with two parameters:
# 1. type of the class whose WRO parent view you're trying to access
# 2. the instance on which to access that view
class ExplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super(ExplicitTrisect, self).__init__(value)
        self.value /= 3


class AutomaticTrisect(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value)
        self.value /= 3


class ImplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value /= 3


# All three ways do the same thing
assert ExplicitTrisect(9).value == 3
assert AutomaticTrisect(9).value == 3
assert ImplicitTrisect(9).value == 3

# The only time you should provide parameters to super is in situations where
# you need to access the specific functionality of a superclass's implementation
# from a child class(eg. to wrap or reuse functionality)
