import re

from .utils import read_file


class Stacks:
    def __init__(self, stacks):
        self.stacks = stacks

    def move9000(self, n, src_id, dest_id):
        src = self.stacks[src_id]
        dest = self.stacks[dest_id]

        for i in range(n):
            dest.append(src.pop())

    def move9001(self, n, src_id, dest_id):
        src = self.stacks[src_id]
        dest = self.stacks[dest_id]

        dest += src[-n:]
        del src[-n:]

    def tops(self):
        return "".join([s[-1] for s in self.stacks])


def test_move():
    stacks = Stacks([["Z", "N"], ["M", "C", "D"], ["P"]])
    stacks.move9000(1, 1, 0)
    assert stacks.stacks[0] == ["Z", "N", "D"]
    assert stacks.stacks[1] == ["M", "C"]


def read_input(text):
    reading_stacks = True
    stacks = []
    moves = []

    for line in text:
        if reading_stacks:
            if line != "":
                stacks.append(line)
            else:
                reading_stacks = False
        elif match := re.match(r"move (\d+) from (\d+) to (\d+)", line):
            moves.append(
                (int(match.group(1)), int(match.group(2)) - 1, int(match.group(3)) - 1)
            )

    return stacks, moves


def test_read_input():
    example = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

    stacks, moves = read_input(example.split("\n"))
    assert moves == [(1, 1, 0), (3, 0, 2), (2, 1, 0), (1, 0, 1)]


def process_stacks(stacks):
    count = int((len(stacks[0]) + 1) / 4)

    only_letters = [
        "".join([stack[i * 4 + 1] for i in range(count)]) for stack in stacks[:-1]
    ]

    transposed = [
        [letter for letter in stack if letter != " "]
        for stack in list(zip(*reversed(only_letters)))
    ]

    return transposed


def test_process_stacks():
    stacks = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 """
    assert process_stacks(stacks.split("\n")) == [["Z", "N"], ["M", "C", "D"], ["P"]]


def do_process(lines, is_9000=True):
    stacks, moves = read_input(lines)
    port = Stacks(process_stacks(stacks))

    for move in moves:
        if is_9000:
            port.move9000(*move)
        else:
            port.move9001(*move)

    return port.tops()


def test_do_process():
    example = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

    assert do_process(example.split("\n"), is_9000=True) == "CMZ"
    assert do_process(example.split("\n"), is_9000=False) == "MCD"


def test_input():
    assert (
        do_process(read_file("inputs/day_5.txt", skip_empty=False), is_9000=True)
        == "QNNTGTPFN"
    )
    assert (
        do_process(read_file("inputs/day_5.txt", skip_empty=False), is_9000=False)
        == "GGNPJBTTR"
    )
