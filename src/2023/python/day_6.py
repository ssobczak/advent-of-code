from copy import copy
from typing import List, Iterator
from functools import reduce

data = """Time:      7  15   30
Distance:  9  40  200"""


def parse(data):
    times = [int(n.strip()) for n in data[0].split(":")[1].strip().split()]
    distances = [int(n.strip()) for n in data[1].split(":")[1].strip().split()]

    return zip(times, distances)


def wins(time, distance):
    return sum(1 for hold in range(time) if (time - hold) * hold > distance)


def part1(data):
    return [wins(time, distance) for time, distance in data]


def test_part1():
    td = parse(data.splitlines(keepends=False))
    assert part1(td) == [4, 8, 9]


def test_part2():
    assert wins(71530, 940200) == 71503


def test_final():
    data = """Time:        38     67     76     73
Distance:   234   1027   1157   1236"""
    td = parse(data.splitlines(keepends=False))

    print(reduce(lambda a, b: a * b, part1(td)))
    print(wins(38677673, 234102711571236))
