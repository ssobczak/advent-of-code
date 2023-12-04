import os
from dataclasses import dataclass

from src.helpers import read_file


@dataclass
class Point:
    right: int
    down: int


class RopeSegment:
    def __init__(self, next_segment=None):
        self.pos = Point(0, 0)
        self.next_segment = next_segment

    def propagate(self):
        if self.next_segment:
            self.next_segment.follow(self.pos)

    def move(self, direction):
        if direction == "U":
            self.pos.down -= 1

        elif direction == "D":
            self.pos.down += 1

        elif direction == "L":
            self.pos.right -= 1

        elif direction == "R":
            self.pos.right += 1

        self.propagate()

    def _align_right(self, parent_pos):
        if parent_pos.right > self.pos.right:
            self.pos.right += 1
        elif parent_pos.right < self.pos.right:
            self.pos.right -= 1

    def _align_down(self, parent_pos):
        if parent_pos.down > self.pos.down:
            self.pos.down += 1
        elif parent_pos.down < self.pos.down:
            self.pos.down -= 1

    def follow(self, parent_pos):
        if parent_pos.down - self.pos.down == 2:
            self.pos.down += 1
            self._align_right(parent_pos)
        if parent_pos.down - self.pos.down == -2:
            self.pos.down -= 1
            self._align_right(parent_pos)

        if parent_pos.right - self.pos.right == 2:
            self.pos.right += 1
            self._align_down(parent_pos)
        if parent_pos.right - self.pos.right == -2:
            self.pos.right -= 1
            self._align_down(parent_pos)

        self.propagate()

    def sequence(self, lines):
        for line in lines:
            direction, times = line.split(" ")
            for _ in range(int(times)):
                self.move(direction)


class RopeTail(RopeSegment):
    def __init__(self):
        super().__init__()
        self.visited = set()

    def follow(self, direction):
        super().follow(direction)
        self.visited.add((self.pos.down, self.pos.right))

    def score(self):
        return len(self.visited)

    def print(self):
        min_down = min(self.visited, key=lambda x: x[0])[0]
        max_down = max(self.visited, key=lambda x: x[0])[0]

        min_right = min(self.visited, key=lambda x: x[1])[1]
        max_right = max(self.visited, key=lambda x: x[1])[1]

        print()
        for down in range(min_down, max_down + 1):
            for right in range(min_right, max_right + 1):
                if (down, right) in self.visited:
                    print("#", end="")
                else:
                    print(".", end="")
            print()


def test_move():
    tail = RopeTail()
    rope = RopeSegment(tail)

    rope.move("R")
    assert tail.pos.right == 0
    rope.move("R")
    assert tail.pos.right == 1

    rope.move("U")
    assert tail.pos.right == 1
    assert tail.pos.down == 0

    rope.move("U")
    assert rope.pos.right == 2
    assert rope.pos.down == -2
    assert tail.pos.right == 2
    assert tail.pos.down == -1

    tail.print()


def test_segment_sequence():
    data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
    tail = RopeTail()
    rope = RopeSegment(tail)
    rope.sequence(data.splitlines())
    tail.print()
    assert tail.score() == 13


def test_segment():
    tail = RopeTail()
    rope = RopeSegment(tail)
    rope.sequence(read_file(os.path.dirname(__file__) + "/../inputs/day_9.txt"))
    assert tail.score() == 6011


def test_long_rope():
    data = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

    head = tail = RopeTail()
    for i in range(9):
        head = RopeSegment(head)

    head.sequence(data.splitlines())
    assert tail.score() == 36
    tail.print()


def test_final():
    head = tail = RopeTail()
    for i in range(9):
        head = RopeSegment(head)
    head.sequence(read_file(os.path.dirname(__file__) + "/../inputs/day_9.txt"))
    assert tail.score() == 2419
