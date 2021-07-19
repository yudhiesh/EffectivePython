class Date:
    def __init__(self, month, day, year) -> None:
        self.month = month
        self.day = day
        self.year = year

    def display(self):
        return f"{self.day}-{self.month}-{self.year}"

    @classmethod
    def from_string(cls, date_as_string: str):
        day, month, year = map(int, date_as_string.split("-"))
        return cls(month, day, year)

    @staticmethod
    def is_date_valid(date_as_string: str) -> bool:
        day, month, year = map(int, date_as_string.split("-"))
        return day <= 31 and month <= 12 and year <= 3999

    @staticmethod
    def from_string_static(date_as_string: str):
        day, month, year = map(int, date_as_string.split("-"))
        return Date(month, day, year)


class DateTime(Date):
    def __init__(self, month, day, year) -> None:
        super().__init__(month, day, year)

    def display(self):
        return f"{self.day}-{self.month}-{self.year} - 00:00:00PM"


if __name__ == "__main__":
    date_str = "12-06-2021"
    date = Date.from_string(date_str)
    date2 = Date.from_string_static(date_str)
    datetime1 = DateTime(10, 10, 2021)
    datetime2 = DateTime.from_string(date_str)  # bound to the subclasses class
    datetime3 = DateTime.from_string_static(date_str)  # bound to the original class
    assert isinstance(datetime1, DateTime)
    assert isinstance(datetime2, DateTime)
    assert not isinstance(datetime3, DateTime)
    print(type(datetime3))
    print(type(datetime2))
    print(datetime1.display())
    print(datetime2.display())
    print(datetime3.display())
