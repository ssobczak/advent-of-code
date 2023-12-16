import os
from collections import defaultdict, deque
from functools import lru_cache
from hashlib import md5

from src.helpers import read_file

N = 0
E = 1
S = 2
W = 3


class Beam:
    def __init__(self, y, x, direction):
        self.y = y
        self.x = x
        self.direction = direction

    def __repr__(self):
        return f"Beam({self.y}, {self.x}, {self.direction})"


def forward(beam, pattern):
    res = []

    if pattern[beam.y][beam.x] == ".":
        if beam.direction == N:
            res.append(Beam(beam.y - 1, beam.x, beam.direction))
        elif beam.direction == E:
            res.append(Beam(beam.y, beam.x + 1, beam.direction))
        elif beam.direction == S:
            res.append(Beam(beam.y + 1, beam.x, beam.direction))
        elif beam.direction == W:
            res.append(Beam(beam.y, beam.x - 1, beam.direction))

    elif pattern[beam.y][beam.x] == "/":
        if beam.direction == N:
            res.append(Beam(beam.y, beam.x + 1, E))
        elif beam.direction == E:
            res.append(Beam(beam.y - 1, beam.x, N))
        elif beam.direction == S:
            res.append(Beam(beam.y, beam.x - 1, W))
        elif beam.direction == W:
            res.append(Beam(beam.y + 1, beam.x, S))

    elif pattern[beam.y][beam.x] == "\\":
        if beam.direction == N:
            res.append(Beam(beam.y, beam.x - 1, W))
        elif beam.direction == E:
            res.append(Beam(beam.y + 1, beam.x, S))
        elif beam.direction == S:
            res.append(Beam(beam.y, beam.x + 1, E))
        elif beam.direction == W:
            res.append(Beam(beam.y - 1, beam.x, N))

    elif pattern[beam.y][beam.x] == "-":
        if beam.direction in (N, S):
            res.append(Beam(beam.y, beam.x - 1, W))
            res.append(Beam(beam.y, beam.x + 1, E))
        elif beam.direction == E:
            res.append(Beam(beam.y, beam.x + 1, E))
        elif beam.direction == W:
            res.append(Beam(beam.y, beam.x - 1, W))

    elif pattern[beam.y][beam.x] == "|":
        if beam.direction in (E, W):
            res.append(Beam(beam.y - 1, beam.x, N))
            res.append(Beam(beam.y + 1, beam.x, S))
        elif beam.direction == N:
            res.append(Beam(beam.y - 1, beam.x, N))
        elif beam.direction == S:
            res.append(Beam(beam.y + 1, beam.x, S))

    return [b for b in res if 0 <= b.y < len(pattern) and 0 <= b.x < len(pattern[0])]


def draw(pattern, visited):
    print()
    for y in range(len(pattern)):
        for x in range(len(pattern[y])):
            if pattern[y][x] == ".":
                if any(visited[y][x]):
                    print("#", end="")
                else:
                    print(".", end="")
            else:
                print(pattern[y][x], end="")
        print()


def part1(pattern, start: Beam):
    beams = deque([start])

    visited = [[[False] * 4 for x in pattern[0]] for y in pattern]
    visited[start.y][start.x][start.direction] = True

    while beams:
        b = beams.popleft()
        for n in forward(b, pattern):
            if visited[n.y][n.x][n.direction]:
                continue

            visited[n.y][n.x][n.direction] = True
            beams.append(n)

        # draw(pattern, visited)

    return sum(sum(1 for d in line if any(d)) for line in visited)


def part2(pattern):
    res = 0

    for y in range(len(pattern)):
        res = max(
            res,
            part1(pattern, Beam(y, 0, E)),
            part1(pattern, Beam(y, len(pattern[0]) - 1, W)),
        )

    for x in range(len(pattern[0])):
        res = max(
            res,
            part1(pattern, Beam(0, x, S)),
            part1(pattern, Beam(len(pattern) - 1, x, N)),
        )

    return res


EXAMPLE = """.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""


def test_part1():
    plane = EXAMPLE.splitlines()
    assert part1(plane, Beam(0, 0, E)) == 46

    data = list(read_file(os.path.dirname(__file__) + "/../inputs/day_16.txt"))
    assert part1(data, Beam(0, 0, E)) == 7870


def test_part2():
    plane = EXAMPLE.splitlines()
    assert part2(plane) == 51

    data = list(read_file(os.path.dirname(__file__) + "/../inputs/day_16.txt"))
    assert part2(data) == 8143
