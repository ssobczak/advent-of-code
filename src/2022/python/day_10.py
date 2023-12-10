import os

from src.helpers import read_file


class Computer:
    def __init__(self):
        self.registry = 1
        self.cycle = 0
        self.total_signal = 0

    def _try_emit_signal(self):
        if self.cycle == 20 or (self.cycle - 20) % 40 == 0:
            # print(self.cycle, self.cycle * self.registry)
            self.total_signal += self.cycle * self.registry

    def _get_sprite(self):
        cycle_line = self.cycle % 40
        if abs(cycle_line - self.registry - 1) <= 1:  # 3 px wide
            return "#"
        else:
            return "."

    def _crt_draw(self):
        if self.cycle % 40 == 0:
            print(self._get_sprite())
        else:
            print(self._get_sprite(), end="")

    def noop(self):
        self.cycle += 1
        self._crt_draw()
        self._try_emit_signal()

    def addx(self, x):
        self.cycle += 1
        self._crt_draw()
        self._try_emit_signal()

        self.cycle += 1
        self._crt_draw()
        self._try_emit_signal()
        self.registry += x

    def run(self, lines):
        print()
        for line in lines:
            command, *args = line.split()
            getattr(self, command)(*map(int, args))


def test_short():
    data = """noop
addx 3
addx -5"""

    computer = Computer()
    computer.run(data.splitlines())
    assert computer.registry == -1


def test_long():
    data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

    computer = Computer()
    computer.run(data.splitlines())
    assert computer.total_signal == 13140


def test_input():
    computer = Computer()
    computer.run(read_file(os.path.dirname(__file__) + "/../inputs/day_10.txt.txt"))
    assert computer.total_signal == 14160
    # prints RJERPEFC
