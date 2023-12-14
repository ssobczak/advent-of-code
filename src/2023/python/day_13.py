import os
from functools import lru_cache

from src.helpers import read_file


def symetric_x(pattern, i, a):
    if i == len(pattern) - 1:
        return False

    for j in range(len(pattern)):
        if i - j < 0:
            return a < i + j + 1
        if i + j + 1 >= len(pattern):
            return a > i - j

        if pattern[i - j] != pattern[i + j + 1]:
            return False

    return False


def test_symetric_x():
    assert symetric_x("#.##..##.", 1, 1) is False
    assert symetric_x("#.##..##.", 4, 4) is True

    data = [
        "#...##..#",
        "#....#..#",
        "..##..###",
        "#####.##.",
        "#####.##.",
        "..##..###",
        "#....#..#",
    ]

    assert symetric_x(data, 3, 3) is True


def symetric_y(pattern, i, b):
    if i == len(pattern[0]) - 1:
        return False

    for j in range(len(pattern[0])):
        if i - j < 0:
            return b < i + j + 1
        if i + j + 1 >= len(pattern[0]):
            return b > i - j

        c1 = [p[i - j] for p in pattern]
        c2 = [p[i + j + 1] for p in pattern]

        if c1 != c2:
            return False

    return False


def opposite(symbol):
    if symbol == "#":
        return "."
    else:
        return "#"


def part1(pattern):
    for i in range(len(pattern)):
        if symetric_x(pattern, i, i):
            return (i + 1) * 100

    for j in range(len(pattern[0])):
        if symetric_y(pattern, j, j):
            return j + 1

    raise Exception("No symetric")


def part2(pattern):
    for a in range(len(pattern)):
        for b in range(len(pattern[a])):
            pattern[a][b] = opposite(pattern[a][b])

            for i in range(len(pattern)):
                if symetric_x(pattern, i, a):
                    return (i + 1) * 100

            for j in range(len(pattern[0])):
                if symetric_y(pattern, j, b):
                    return j + 1

            pattern[a][b] = opposite(pattern[a][b])

    raise Exception("No symetric")


def parse(data, func):
    pattern = []
    res = 0
    for line in data:
        if line == "":
            res += func([list(p) for p in pattern])
            pattern = []
        else:
            pattern.append(line)

    return res + func([list(p) for p in pattern])


EXAMPLE = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def test_part1():
    assert parse(EXAMPLE.splitlines(keepends=False), part1) == 405

    data = list(
        read_file(os.path.dirname(__file__) + "/../inputs/day_13.txt", skip_empty=False),
    )
    assert parse(data, part1) == 35521


def test_part2():
    assert parse(EXAMPLE.splitlines(keepends=False), part2) == 400

    data = list(read_file(os.path.dirname(__file__) + "/../inputs/day_13.txt", skip_empty=False))
    assert parse(data, part2) == 34795
