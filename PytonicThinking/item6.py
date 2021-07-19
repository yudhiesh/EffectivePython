snack_calories = {
    "chips": 140,
    "popcorn": 80,
    "nuts": 190,
}
items = tuple(snack_calories.items())
print(items)
# Unpacking values from a tuple
item = ("Peanut butter", "Jelly")
first, second = item  # Unpacking
print(first, "and", second)

# Unpacking can be used to swap values in place without the need to create temporary values


def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):
            if a[i] < a[i - 1]:
                a[i - 1], a[i] = a[i], a[i - 1]


names = ["pretzels", "carrots", "arugula", "bacon"]
bubble_sort(names)
print(names)

snacks = [("bacon", 350), ("donut", 240), ("muffin", 190)]
for rank, (name, calories) in enumerate(snacks, 1):
    print(f"#{rank}: {name} has {calories} calories")
