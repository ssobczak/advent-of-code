import os

from src.helpers import read_file


class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    @staticmethod
    def from_string(range_str: str) -> "Range":
        start, end = range_str.split("-")
        return Range(int(start), int(end))

    def contais(self, other: "Range") -> bool:
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other: "Range") -> bool:
        if self.start <= other.start:
            left = self
            right = other
        else:
            left = other
            right = self

        return right.start <= left.end


def test_contais():
    assert Range(2, 8).contais(Range(3, 7))


def test_overlaps():
    assert Range(2, 8).overlaps(Range(2, 2))
    assert Range(2, 8).overlaps(Range(3, 7))
    assert Range(2, 8).overlaps(Range(3, 10))
    assert Range(2, 8).overlaps(Range(8, 10))
    assert not Range(2, 8).overlaps(Range(9, 10))

    assert Range(2, 2).overlaps(Range(2, 8))
    assert Range(3, 7).overlaps(Range(2, 8))
    assert Range(3, 10).overlaps(Range(2, 8))
    assert Range(8, 10).overlaps(Range(2, 8))
    assert not Range(9, 10).overlaps(Range(2, 8))

    assert Range(2, 2).overlaps(Range(2, 2))
    assert Range(2, 8).overlaps(Range(3, 3))
    assert not Range(2, 2).overlaps(Range(1, 1))


def count_containing(lines):
    res = 0
    for line in lines:
        t1, t2 = line.split(",")
        r1 = Range.from_string(t1)
        r2 = Range.from_string(t2)

        if r1.contais(r2) or r2.contais(r1):
            res += 1
    return res


def count_overlapping(lines):
    res = 0

    for line in lines:
        t1, t2 = line.split(",")
        r1 = Range.from_string(t1)
        r2 = Range.from_string(t2)

        if r1.overlaps(r2):
            res += 1

    return res


def test_counts():
    example = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

    assert count_containing(example.split("\n")) == 2
    assert count_overlapping(example.split("\n")) == 4


def test_input():
    data = read_file(os.path.dirname(__file__) + "/../inputs/day_4.txt")
    assert count_containing(data) == 498

    data = read_file(os.path.dirname(__file__) + "/../inputs/day_4.txt")
    assert count_overlapping(data) == 859
