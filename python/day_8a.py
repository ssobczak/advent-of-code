from utils import read_file


def rotate(matrix):
    return [list(row) for row in zip(*matrix[::-1])]


def test_rotate():
    data = [
        [1, 2],
        [3, 4],
    ]
    assert rotate(data) == [
        [3, 1],
        [4, 2],
    ]


def count_visible(matrix, visible):
    for row in range(len(matrix)):
        max_so_far = -1
        for col in range(len(matrix[row])):
            if matrix[row][col] > max_so_far:
                max_so_far = matrix[row][col]
                visible[row][col] = 1

    return visible


def test_count_visible():
    data = [
        (3, 2),
        (4, 3),
    ]
    visible = [[0, 0], [0, 0]]
    assert count_visible(data, visible) == [[1, 0], [1, 0]]


def read(lines):
    matrix = []
    visible = []

    for line in lines:
        matrix.append([int(height) for height in line])
        visible.append([0] * len(line))

    for i in range(4):
        visible = count_visible(matrix, visible)
        matrix = rotate(matrix)
        visible = rotate(visible)

    return sum(sum(v for v in row) for row in visible)


def test_read():
    data = """30373
25512
65332
33549
35390"""
    assert read(data.split("\n")) == 21
    assert read(read_file("../inputs/day_8.txt")) == 1703
