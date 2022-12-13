from functools import cmp_to_key

from .utils import read_file


def pairwise(items):
    it = iter(items)
    return zip(it, it)


def cmp(l, r):
    if isinstance(l, int) and isinstance(r, int):
        return 0 if l == r else 1 if l < r else -1
    if isinstance(l, list) and isinstance(r, int):
        return cmp(l, [r])
    if isinstance(l, int) and isinstance(r, list):
        return cmp([l], r)
    if isinstance(l, list) and isinstance(r, list):
        if len(l) == 0 or len(r) == 0:
            return 0 if len(l) == len(r) else 1 if len(l) < len(r) else -1
        else:
            if first_elements := cmp(l[0], r[0]):
                return first_elements
            else:
                return cmp(l[1:], r[1:])


def process(input_lines):
    return map(lambda x: cmp(eval(x[0]), eval(x[1])), pairwise(input_lines))


DATA = """[1,1,3,1,1]
[1,1,5,1,1]
[[1],[2,3,4]]
[[1],4]
[9]
[[8,7,6]]
[[4,4],4,4]
[[4,4],4,4,4]
[7,7,7,7]
[7,7,7]
[]
[3]
[[[]]]
[[]]
[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def test_cmp():
    res = process(DATA.split("\n"))
    assert list(res) == [1, 1, -1, 1, -1, 1, -1, -1]


def correctness_score(input_lines):
    return sum(
        line_no + 1
        for line_no, correct in enumerate(process(input_lines))
        if correct == 1
    )


def test_correctness_score():
    assert correctness_score(DATA.split("\n")) == 13
    assert correctness_score(read_file("inputs/day_13.txt")) == 5675


MARKER_2 = [[2]]
MARKER_6 = [[6]]


def with_dividers(input_lines):
    return [eval(line) for line in input_lines] + [MARKER_2, MARKER_6]


def ordered_score(input_lines):
    sorted_lines = sorted(with_dividers(input_lines), key=cmp_to_key(cmp), reverse=True)
    return (sorted_lines.index(MARKER_2) + 1) * (sorted_lines.index(MARKER_6) + 1)


def test_ordered_score():
    assert ordered_score(DATA.split("\n")) == 140
    assert ordered_score(read_file("inputs/day_13.txt")) == 20383