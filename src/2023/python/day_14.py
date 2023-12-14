import os
from functools import lru_cache
from hashlib import md5

from src.helpers import read_file


def calc(pattern):
    res = 0
    for i, line in enumerate(pattern):
        for j, symbol in enumerate(line):
            if symbol == "O":
                res += len(pattern) - i

    return res


def tilt_north(pattern):
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            if pattern[i][j] == "O":
                for mov in range(1, i + 1):
                    if pattern[i - mov][j] == ".":
                        pattern[i - mov][j] = "O"
                        pattern[i - mov + 1][j] = "."
                    else:
                        break

    return pattern


def tilt_south(pattern):
    for i in range(len(pattern) - 1, -1, -1):
        for j in range(len(pattern[0])):
            if pattern[i][j] == "O":
                for mov in range(1, len(pattern) - i):
                    if pattern[i + mov][j] == ".":
                        pattern[i + mov][j] = "O"
                        pattern[i + mov - 1][j] = "."
                    else:
                        break
    return pattern


def tilt_west(pattern):
    for j in range(len(pattern[0])):
        for i in range(len(pattern)):
            if pattern[i][j] == "O":
                for mov in range(1, j + 1):
                    if pattern[i][j - mov] == ".":
                        pattern[i][j - mov] = "O"
                        pattern[i][j - mov + 1] = "."
                    else:
                        break

    return pattern


def tilt_east(pattern):
    for j in range(len(pattern[0]) - 1, -1, -1):
        for i in range(len(pattern)):
            if pattern[i][j] == "O":
                for mov in range(1, len(pattern[0]) - j):
                    if pattern[i][j + mov] == ".":
                        pattern[i][j + mov] = "O"
                        pattern[i][j + mov - 1] = "."
                    else:
                        break

    return pattern


def signature(pattern):
    return hash("".join("".join(s) for s in pattern))


def cycle(pattern):
    pattern = tilt_north(pattern)
    pattern = tilt_west(pattern)
    pattern = tilt_south(pattern)
    pattern = tilt_east(pattern)

    return pattern


def part2(pattern, n):
    patterns = {}

    curr = 0
    curr_sign = ""
    while curr_sign not in patterns:
        patterns[curr_sign] = curr
        curr += 1
        pattern = cycle(pattern)
        curr_sign = signature(pattern)

    cycle_len = curr - patterns[curr_sign]
    next = n - curr
    for i in range(next % cycle_len):
        pattern = cycle(pattern)

    return calc(pattern)


EXAMPLE = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


def test_part1():
    test_data = [list(s) for s in EXAMPLE.splitlines(keepends=False)]
    assert calc(tilt_north(test_data)) == 136

    input = [list(s) for s in read_file(os.path.dirname(__file__) + "/../inputs/day_14.txt")]
    assert calc(tilt_north(input)) == 110128


def test_part2():
    test_data = [list(s) for s in EXAMPLE.splitlines(keepends=False)]
    assert part2(test_data, 1000000000) == 64

    input = [list(s) for s in read_file(os.path.dirname(__file__) + "/../inputs/day_14.txt")]
    assert part2(input, 1000000000) == 103861
