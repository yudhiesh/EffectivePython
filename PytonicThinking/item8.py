import itertools

# Using zip() to process iterators in parallel
names = ["Cecilia", "Lise", "Marie"]
counts = [len(n) for n in names]

names.append("Rosalia")
for name, count in zip(names, counts):
    print(name)

# zip_longest replaces missing values as names and counts do not have the same
# length
# Missing values are replaced with None by default
for name, count in itertools.zip_longest(names, counts):
    print(f"{name} : {count}")
