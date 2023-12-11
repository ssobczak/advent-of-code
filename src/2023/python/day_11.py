import os
from src.helpers import read_file


def dist_with_expansion(a, b, expanded, expansion):
    dist = 0
    for i in range(min(a, b), max(a, b)):
        if i in expanded:
            dist += expansion
        else:
            dist += 1
    return dist


def foo(data, expansion):
    dup_rows = set(range(len(data)))
    dup_cols = set(range(len(data[0])))

    galaxies = []
    for i, line in enumerate(data):
        for j, val in enumerate(line):
            if val == "#":
                galaxies.append((i, j))
                dup_rows.discard(i)
                dup_cols.discard(j)

    res = 0
    for a in range(len(galaxies)):
        for b in range(a + 1, len(galaxies)):
            dist = dist_with_expansion(galaxies[a][0], galaxies[b][0], dup_rows, expansion)
            dist += dist_with_expansion(galaxies[a][1], galaxies[b][1], dup_cols, expansion)
            # print(a, b, dist)
            res += dist

    return res


def test_foo():
    data = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    assert foo(data.splitlines(), expansion=2) == 374
    assert foo(data.splitlines(), expansion=10) == 1030
    assert foo(data.splitlines(), expansion=100) == 8410

    data = list(read_file(os.path.dirname(__file__) + "/../inputs/day_11.txt"))
    assert foo(data, expansion=2) == 9445168
    assert foo(data, expansion=1_000_000) == 742305960572
