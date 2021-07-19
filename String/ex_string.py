import datetime


class Car:
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage

    # def __str__(self):
    #     return f"a {self.color} car with {self.mileage}km"

    # Python will always fall back to the repr
    # If there are str and repr then str will be used instead
    # !r is the same as repr(self.color)
    def __repr__(self):
        return (
            f"{self.__class__.__name__}" f"({self.color!r} car with {self.mileage!r}km)"
        )


# The result of the __str__ function should primarily be readable
# With __repr__ the idea is that its result should be, above all unambiguous
# In essence it needs to be explicit as possible about what this object is
car = Car("Green", 100)
print(car)
