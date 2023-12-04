import os

from src.helpers import read_file


class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

        self.weight = 0
        self.children = {}

    def get_total_weight(self):
        return self.weight + sum(
            child.get_total_weight() for child in self.children.values()
        )

    def print(self, prefix=""):
        current = f"{prefix}{self.name}/"

        yield current, self.get_total_weight()
        for child in self.children.values():
            yield from child.print(current)


def read(lines):
    cwd = Dir("~", None)

    for line in lines:
        if line == "$ cd /":
            continue

        parts = line.split(" ")
        if parts[0] == "$":
            if parts[1] == "ls":
                pass
            elif parts[1] == "cd":
                if parts[2] == "..":
                    cwd = cwd.parent
                else:
                    cwd = cwd.children[parts[2]]

        # LS-ing
        elif parts[0].isnumeric():
            cwd.weight += int(parts[0])
        else:
            if not cwd.children.get(parts[1]):
                cwd.children[parts[1]] = Dir(parts[1], cwd)

    while cwd.parent:
        cwd = cwd.parent

    return cwd


def test_read():
    example = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
    fs = read(example.split("\n"))
    res = list(fs.print())
    assert res == [
        ("~/", 48381165),
        ("~/a/", 94853),
        ("~/a/e/", 584),
        ("~/d/", 24933642),
    ]


def test_input_a():
    fs = read(read_file(os.path.dirname(__file__) + "/../inputs/day_7.txt"))
    res = sum(size for name, size in fs.print() if size < 100_000)
    assert res == 1611443


def test_input_b():
    fs = read(read_file(os.path.dirname(__file__) + "/../inputs/day_7.txt"))
    taken = fs.get_total_weight()

    needed = taken + 30_000_000 - 70_000_000
    res = min(size for name, size in fs.print() if needed < size)

    assert res == 2086088
