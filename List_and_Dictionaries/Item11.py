from collections import defaultdict

x = ["a", "b", "c", "d", "e", "f", "g", "h"]

print(x[::2])
print(x[::-2])
print(x[2::2])
print(x[-2::-2])
print(x[-2:2:-2])
print(x[2:2:-2])

car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)
oldest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others)
# 20 19 [15, 9, 8, 7, 6, 4, 1, 0]

car_inventory = {
    "Downtown": ("Silver Shadow", "Pinto", "DMC"),
    "Airport": ("Skyline", "Viper", "Gremlin", "Nova"),
}
((loc1, (best1, *rest1)), (loc2, (best2, *rest2))) = car_inventory.items()
print(f"Best at {loc1} is {best1}, {len(rest1)} others")
print(f"Best at {loc2} is {best2}, {len(rest2)} others")


class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return f"Tool({self.name!r}, {self.weight})"


tools = [
    Tool("level", 3.5),
    Tool("hammer", 1.25),
    Tool("screwdriver", 0.5),
    Tool("chisel", 0.25),
]

print("\nUnsorted: ", repr(tools))
tools.sort(key=lambda x: x.weight)
print("\nSorted: ", tools)

places = ["home", "work", "New York", "Paris"]
places.sort()
print("Case sensitive: ", places)
places.sort(key=lambda x: x.lower())
print("Case insensitive:", places)

# Tuples have a natural ordering to them
saw = (5, "circular saw")
jackhammer = (40, "jackhammer")
assert not (jackhammer < saw)

power_tools = [
    Tool("drill", 4),
    Tool("circular saw", 5),
    Tool("jackhammer", 40),
    Tool("sander", 4),
]
power_tools.sort(key=lambda x: (x.weight, x.name), reverse=True)
print(power_tools)


data = {}
key = "foo"
value = []
data.setdefault(key, value)
print("Before", data)
value.append("hello")
print("After", data)


class Visits(object):
    def __init__(self):
        self.data = defaultdict(set)

    def add(self, country, city):
        self.data[country].add(city)


visits = Visits()
visits.add("England", "Bath")
visits.add("England", "London")
visits.add("Malaysia", "Kuala Lumpur")
visits.add("Malaysia", "Penang")

path = "profile_1234.png"


def open_picture(profile_path):
    try:
        return open(profile_path, "a+b")
    except OSError:
        print(f"Failed to open {profile_path}")
        raise


class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value


pictures = Pictures()
handle = pictures[path]
handle.seek(0)
image_data = handle.read()
