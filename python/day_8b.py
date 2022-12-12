from utils import read_file


def visibility(data, row, col):
    top_vis = 0
    for i in range(row - 1, -1, -1):
        top_vis += 1
        if data[i][col] >= data[row][col]:
            break

    bottom_vis = 0
    for i in range(row + 1, len(data)):
        bottom_vis += 1
        if data[i][col] >= data[row][col]:
            break

    left_vis = 0
    for i in range(col - 1, -1, -1):
        left_vis += 1
        if data[row][i] >= data[row][col]:
            break

    right_vis = 0
    for i in range(col + 1, len(data[row])):
        right_vis += 1
        if data[row][i] >= data[row][col]:
            break

    # print(data[row][col])
    # print(top_vis, left_vis, right_vis, bottom_vis)
    return top_vis * bottom_vis * left_vis * right_vis


def best_tree(data):
    return max(
        visibility(data, row, col)
        for row in range(len(data))
        for col in range(len(data[row]))
    )


def test_visibility():
    data = """30373
25512
65332
33549
35390"""

    assert visibility(data.split("\n"), 1, 2) == 4
    assert visibility(data.split("\n"), 3, 2) == 8


def test_best_score():
    data = """30373
25512
65332
33549
35390"""

    assert best_tree(data.split("\n")) == 8
    assert best_tree(list(read_file("../inputs/day_8.txt"))) == 496650
