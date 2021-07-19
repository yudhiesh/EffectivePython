from collections import namedtuple
from typing import NamedTuple

Car = namedtuple("Car", "color mileage automatic")

car1 = Car("blue", 10_000, True)
car2 = Car("green", 232_323, False)


class House(NamedTuple):
    color: str
    price: int
    for_sale: bool


house = House("Black", 1_000_000, False)
print(house)
