import math
import os
from functools import cached_property

from src.helpers import read_file


class Node:
    def __init__(self, map, x, y):
        self.map = map
        self.x = x
        self.y = y

    @property
    def symbol(self):
        if self.x < 0 or self.y < 0 or self.y >= len(self.map) or self.x >= len(self.map[self.y]):
            return "."

        return self.map[self.y][self.x]

    @property
    def pipe_symbol(self):
        if self.symbol == "S":
            return self.s_pipe()

        return self.symbol

    def s_pipe(self):
        if self.map.known_start_symbol:
            return self.map.known_start_symbol

        adjecent = {
            "U": (self.x, self.y - 1),
            "D": (self.x, self.y + 1),
            "L": (self.x - 1, self.y),
            "R": (self.x + 1, self.y),
        }

        dirs = set()
        for direction, adj in adjecent.items():
            if self in Node(self.map, *adj).neighbors():
                dirs.add(direction)

        if dirs == {"U", "D"}:
            return "|"
        elif dirs == {"L", "R"}:
            return "-"
        elif dirs == {"U", "R"}:
            return "L"
        elif dirs == {"U", "L"}:
            return "J"
        elif dirs == {"D", "L"}:
            return "7"
        elif dirs == {"D", "R"}:
            return "F"
        else:
            raise Exception("Invalid S")

    def neighbors(self):
        if self.pipe_symbol == "-":
            return Node(self.map, self.x - 1, self.y), Node(self.map, self.x + 1, self.y)
        elif self.pipe_symbol == "|":
            return Node(self.map, self.x, self.y - 1), Node(self.map, self.x, self.y + 1)
        elif self.pipe_symbol == "L":
            return Node(self.map, self.x, self.y - 1), Node(self.map, self.x + 1, self.y)
        elif self.pipe_symbol == "J":
            return Node(self.map, self.x, self.y - 1), Node(self.map, self.x - 1, self.y)
        elif self.pipe_symbol == "7":
            return Node(self.map, self.x, self.y + 1), Node(self.map, self.x - 1, self.y)
        elif self.pipe_symbol == "F":
            return Node(self.map, self.x, self.y + 1), Node(self.map, self.x + 1, self.y)
        elif self.pipe_symbol in (".", " "):
            return ()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.symbol})"

    def __hash__(self):
        return hash((self.x, self.y))


class Map:
    def __init__(self, map, known_start_symbol=None):
        self.map = map
        self.known_start_symbol = known_start_symbol

    def __getitem__(self, item):
        return self.map[item]

    def __len__(self):
        return len(self.map)

    def find_start(self):
        for y, line in enumerate(self.map):
            for x, symbol in enumerate(line):
                if symbol == "S":
                    return x, y

    def find_loop(self):
        nodes = [Node(self, *self.find_start())]

        while True:
            for node in nodes[-1].neighbors():
                if node.symbol == ".":
                    print(len(nodes), node)
                    continue

                if node.symbol == "S" and len(nodes) > 2:
                    return nodes

                if node not in nodes:
                    nodes.append(node)
                    break

    def __repr__(self):
        return "\n".join("".join(line) for line in self.map)

    def prune_loop(self):
        loop = set(self.find_loop())

        for y, row in enumerate(self.map):
            for x, symbol in enumerate(row):
                if Node(self, x, y) not in loop:
                    self.map[y][x] = "."

    def clean_external(self):
        to_visit = [(0, 0)]

        while to_visit:
            curr = to_visit.pop()
            self.map[curr[1]][curr[0]] = " "

            for next in (
                (curr[0] + 1, curr[1]),
                (curr[0] - 1, curr[1]),
                (curr[0], curr[1] + 1),
                (curr[0], curr[1] - 1),
            ):
                if next[0] >= 0 and next[1] >= 0 and next[0] < len(self.map[0]) and next[1] < len(self.map):
                    if self.map[next[1]][next[0]] == ".":
                        to_visit.append(next)


def part1(data) -> int:
    map = Map([list(line) for line in data])
    loop = map.find_loop()
    return math.floor(len(loop) / 2)


def grow(map):
    res = ["." * (len(map[0]) * 2 + 1)]

    for row in map:
        new_row = ["."]
        for symbol in row:
            new_row += symbol + "-"
        res.append(new_row)
        res.append(["|"] * (len(row) * 2 + 1))

    return res


def shrink(map):
    res = []

    for y in range(1, len(map), 2):
        res.append([])
        for x in range(1, len(map[y]), 2):
            res[-1].append(map[y][x])

    return res


def part2(data) -> int:
    small_map = Map([list(line) for line in data])
    start = Node(small_map, *small_map.find_start())

    print(start)

    grown_data = grow(data)
    grown_map = Map([list(line) for line in grown_data], known_start_symbol=start.s_pipe())
    grown_map.prune_loop()

    print(grown_map)
    grown_map.clean_external()
    print(grown_map)

    shrunk = shrink(grown_map.map)
    shrunk_map = Map([list(line) for line in shrunk], known_start_symbol=start.s_pipe())
    print(shrunk_map)

    res = 0
    for y, row in enumerate(shrunk_map.map):
        for x, symbol in enumerate(row):
            if symbol == ".":
                res += 1
    return res


if __name__ == "__main__":
    data = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
    # assert part2(data.splitlines()) == 1

    print(part2(list(read_file(os.path.dirname(__file__) + "/../inputs/day_10.txt"))))
