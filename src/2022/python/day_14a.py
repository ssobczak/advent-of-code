import os
from dataclasses import dataclass
from typing import List

import pytest

from src.helpers import read_file


@dataclass(eq=True)
class Point:
    down: int
    right: int


class Cave:
    def __init__(self, height, width, extend):
        self.map = [["."] * width for _ in range(height)]
        self.extend = extend
        self.start = 500
        self.grains = 0

    @staticmethod
    def from_lines(lines_text, extend=False):
        rocks = []
        for i, line in enumerate(lines_text):
            rocks.append([])
            for path in line.split(" -> "):
                x, y = path.split(",")
                rocks[i].append(Point(int(y), int(x)))

        width = max([max([point.right for point in rock]) for rock in rocks]) + 1
        height = max([max([point.down for point in rock]) for rock in rocks]) + 1

        cave = Cave(height, width, extend)
        for line in rocks:
            cave.add_line(line)

        if extend:
            cave.map.append(["."] * width)
            cave.map.append(["#"] * width)

        return cave

    def extend_right(self):
        for line in self.map[:-1]:
            line.append(".")
        self.map[-1].append("#")

    def extend_left(self):
        for line in self.map[:-1]:
            line.insert(0, ".")
        self.map[-1].insert(0, "#")
        self.start += 1

    def add_line(self, line: List[Point]):
        start = line[0]

        for end in line[1:]:
            while start != end:
                self.map[start.down][start.right] = "#"

                if start.down < end.down:
                    start = Point(start.down + 1, start.right)
                elif start.down > end.down:
                    start = Point(start.down - 1, start.right)
                elif start.right < end.right:
                    start = Point(start.down, start.right + 1)
                elif start.right > end.right:
                    start = Point(start.down, start.right - 1)

            self.map[start.down][start.right] = "#"

    def is_empty(self, down, right):
        if down >= len(self.map) or down < 0:
            return True
        if right >= len(self.map[down]) or right < 0:
            return True

        return self.map[down][right] == "."

    def drop_sand(self):
        pos = Point(0, 500)

        if not self.is_empty(pos.down, pos.right):  # end condition for part 2
            return False

        while True:
            if self.extend:
                if pos.right == 0:
                    self.extend_left()
                elif pos.right == len(self.map[pos.down]) - 1:
                    self.extend_right()

            if pos.down == len(self.map):  # end condition for part 1
                return False

            if self.is_empty(pos.down + 1, pos.right):
                pos = Point(pos.down + 1, pos.right)
            elif self.is_empty(pos.down + 1, pos.right - 1):
                pos = Point(pos.down, pos.right - 1)
            elif self.is_empty(pos.down + 1, pos.right + 1):
                pos = Point(pos.down, pos.right + 1)
            elif self.is_empty(pos.down, pos.right):
                self.map[pos.down][pos.right] = "o"
                self.grains += 1
                return True
            else:
                raise Exception("No way to go")

    def __str__(self):
        return "\n".join(["".join(line) for line in self.map])


DATA = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def test_part1():
    cave = Cave.from_lines(DATA.splitlines())
    while cave.drop_sand():
        pass

    # print("----------------")
    # print(cave)
    assert cave.grains == 24


def test_part2():
    cave = Cave.from_lines(DATA.splitlines(), extend=True)
    while cave.drop_sand():
        pass

    # print()
    # print(cave)
    assert cave.grains == 93


def test_input():
    data = read_file(os.path.dirname(__file__) + "/../inputs/day_14.txt")

    cave = Cave.from_lines(data)
    while cave.drop_sand():
        pass
    assert cave.grains == 578


@pytest.mark.slow
def test_input_ext():
    data = read_file(os.path.dirname(__file__) + "/../inputs/day_14.txt")

    cave = Cave.from_lines(data, extend=True)
    while cave.drop_sand():
        pass
    assert cave.grains == 24377
