import math
import os

from src.helpers import read_file


def foo(numbers):
    rows = [numbers]

    while True:
        last = rows[-1]

        if len(last) == 1 or all([n == 0 for n in last]):
            break

        rows.append([last[i + 1] - last[i] for i in range(len(last) - 1)])

    for r in rows:
        print(r)

    last_digit = 0
    for i in range(2, len(rows) + 1):
        last_digit += rows[-i][-1]

    first_digit = 0
    for i in range(2, len(rows) + 1):
        first_digit = rows[-i][0] - first_digit
        print(first_digit)

    return first_digit


def part1(data):
    res = 0
    for line in data:
        numbers = [int(n) for n in line.split()]
        res += foo(numbers)
    return res


def test_part2():
    data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    assert part1(data.splitlines()) == 2

    print(part1(list(read_file(os.path.dirname(__file__) + "/../inputs/day_9.txt"))))
