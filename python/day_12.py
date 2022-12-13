from collections import deque
from dataclasses import dataclass
from typing import List, Iterator

from .utils import read_file


@dataclass(eq=True, frozen=True)
class Position:
    down: int
    right: int


class Map:
    def __init__(self, lines: List[str]):
        self.map = self.letters_to_heights(lines)

        self.start = next(self.find_positions(self.map, self.char_to_int("S")))
        self.end = next(self.find_positions(self.map, self.char_to_int("E")))

        self.map[self.start.down][self.start.right] = 0
        self.map[self.end.down][self.end.right] = self.char_to_int("z")

    @staticmethod
    def char_to_int(char):
        return ord(char) - ord("a")

    @staticmethod
    def find_positions(lines: List[List], letter) -> Iterator[Position]:
        for i, line in enumerate(lines):
            if letter in line:
                yield Position(down=i, right=line.index(letter))

    @classmethod
    def letters_to_heights(cls, lines: List[str]):
        return [
            list(map(lambda letter: cls.char_to_int(letter), line)) for line in lines
        ]

    def get_neighbours(self, position: Position):
        if position.down > 0:
            yield Position(position.down - 1, position.right)
        if position.down < len(self.map) - 1:
            yield Position(position.down + 1, position.right)

        if position.right > 0:
            yield Position(position.down, position.right - 1)
        if position.right < len(self.map[position.down]) - 1:
            yield Position(position.down, position.right + 1)

    def can_move_to(self, current: Position, neighbour: Position):
        return (
            self.map[neighbour.down][neighbour.right]
            - self.map[current.down][current.right]
            <= 1
        )

    def bfs(self, start: Position):
        queue = deque()
        visited = dict()

        queue.append((start, 0))
        while queue:
            current, depth = queue.popleft()
            if visited.get(current):
                continue
            visited[current] = depth

            if current == self.end:
                return depth

            for neighbour in self.get_neighbours(current):
                if neighbour not in visited and self.can_move_to(current, neighbour):
                    queue.append((neighbour, depth + 1))

    def path_length_from_start(self):
        return self.bfs(self.start)

    def shortest_path(self):
        return min(
            self.bfs(position)
            for position in self.find_positions(self.map, self.char_to_int("a"))
        )


def test_letters_to_heights():
    lines = ["abc", "def"]
    assert Map.letters_to_heights(lines) == [[0, 1, 2], [3, 4, 5]]


def test_read():
    data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

    m = Map(data.splitlines())
    assert m.start == Position(down=0, right=0)
    assert m.end == Position(down=2, right=5)

    assert m.path_length_from_start() == 31
    assert m.shortest_path() == 29


def test_data():
    m = Map(read_file("inputs/day_12.txt"))

    assert m.path_length_from_start() == 408
    assert m.shortest_path() == 399
