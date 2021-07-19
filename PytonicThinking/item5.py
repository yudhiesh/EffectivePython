from urllib.parse import parse_qs

# write helper functions instead of complex expressions
# say I wanted to decode the query string from a URL

my_values = parse_qs("red=5&blue=0&green=", keep_blank_values=True)

print(repr(my_values))
# Some query string parameters may have multiple values and some might not have
# any values

print("Red:     ", my_values.get("red"))
print("Green:   ", my_values.get("green"))
print("Opacity: ", my_values.get("opacity"))

# How do we assign default values when a parameter isn't supplied or is blank
# We could use an entire if statement but there is a shorter way
# Empty strings, empty list and 0 all evaluate to False
# Thus the expression below will evaluate the expression after the "or"
# For query string 'red=5&blue=0&green='

red = my_values.get("red", [""])[0] or 0
green = my_values.get("green", [""])[0] or 0
opacity = my_values.get("opacity", [""])[0] or 0
# !r equates to repr
print(f"Red:     {red!r}")
print(f"Green:   {green!r}")
print(f"Opacity: {opacity!r}")

red_str = my_values.get("red", [""])
red = int(red_str[0]) if red_str[0] else 0
print(f"Red:     {red!r}")


# If the logic needs to be repeated several times then it is best to create a separate function for it
def get_first_int(values, key, default=0):
    found = values.get(key, [""])
    if found[0]:
        return int(found[0])
    return default


green = get_first_int(my_values, "green")
print(f"Green:   {green!r}")
