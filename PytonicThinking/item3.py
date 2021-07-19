# bytes vs str
# both of them represent character data
# bytes contain raw, unsigned 8-bit values which are displayed in ASCII encoding
# str contain Unicode code points that represent textual characters from human languages
# str instances do not have associated binary encoding and bytes instances do not have an associated text encoding
# to convert binary data to Unicode data you must call decode method of bytes and encode for the other way


a = b"h\x65llo"
b = "a\u0300 propos"

print(list(a))
print(a)
print(list(b))
print(b)


def convert_to_str_or_bytes(input):
    if isinstance(input, bytes):
        return input.decode("utf-8")
    elif isinstance(input, str):
        return input.encode("utf-8")


print(repr(convert_to_str_or_bytes(b"h\x65llo")))
print(repr(convert_to_str_or_bytes(b"bar")))
print(repr(convert_to_str_or_bytes(0)))

# you can add bytes and bytes together to concat them and vice versa with str
# but you cannot add bytes and str together
print(b"one" + b"two")
print("one" + "two")

assert b"red" > b"blue"
