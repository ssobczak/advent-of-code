import os

from src.helpers import read_file


def sums(data, n_top):
    res = []
    current = 0

    for row in data:
        if row:
            current += int(row)
        else:
            res.append(current)
            current = 0

    res.sort(reverse=True)
    return sum(res[:n_top])


def test_sums():
    data = list(
        read_file(os.path.dirname(__file__) + "/../inputs/day_1.txt", skip_empty=False)
    )
    assert sums(data, 1) == 75622
    assert sums(data, 3) == 213159
