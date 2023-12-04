words = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_front(row):
    for i in range(len(row)):
        for word, value in words.items():
            if row[i:].startswith(word):
                return str(value)

        if row[i].isdigit():
            return row[i]


def get_back(row):
    for i in range(1, len(row) + 1):
        for word, value in words.items():
            if row[-i:].startswith(word):
                return str(value)

        if row[-i].isdigit():
            return row[-i]


def func(data):
    total = 0
    for row in data.split("\n"):
        res = get_front(row) + get_back(row)

        if len(res) == 1:
            res += res

        total += int(res)
    return total


def test_part_2():
    input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    assert func(input) == 281
