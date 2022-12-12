from collections import deque

from utils import read_file


def find_start(text, n):
    window = deque(text[:n], maxlen=n)

    for i in range(n, len(text)):
        if len(set(window)) == n:
            return i
        else:
            window.append(text[i])


def test_find_start():
    assert find_start("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
    assert find_start("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
    assert find_start("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26

    text = next(read_file("../inputs/day_6.txt"))

    assert find_start(text, 4) == 1702
    assert find_start(text, 14) == 3559
