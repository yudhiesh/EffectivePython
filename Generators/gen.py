# def fib_gen():
#     a, b = 0, 1
#     while True:
#         yield a
#         a, b = b, a + b


# fs = fib_gen()
# print(next(fs))
# for i in range(100):
#     print(next(fs))

# Open the file, iterate through it, and yield a row.
# This does not throw a memeory error
file_name = "/usr/bin/"


def csv_reader(file_name):
    for row in open(file_name, "r"):
        yield row


# csv_gen = (row for row in open(file_name))


def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1


def is_palindrome(num):
    if num // 10 == 0:
        return False
    temp, reversed_num = num, 0

    while temp != 0:
        reversed_num = (reversed_num * 10) + (temp % 10)
        temp = temp // 10

    return True if num == reversed_num else False


def infinite_palindromes():
    num = 0
    while True:
        if is_palindrome(num):
            # yield is an expression rather than a statement
            # this allows you to manipulate the yielded value
            i = yield num
            if i:
                num = i
        num += 1


pal_gen = infinite_palindromes()
for i in pal_gen:
    print(i)
    digits = len(str(i))
    if digits == 5:
        # pal_gen.throw(ValueError("No large palindromes"))
        pal_gen.close()
    pal_gen.send(10 ** (digits))

# for i in infinite_sequence():
#     pal = is_palindrome(i)
#     if pal:
#         print(pal)
