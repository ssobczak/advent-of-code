def neighbors(i, j, data):
    # row above
    if i > 0:
        if j > 0:
            yield i - 1, j - 1

        yield i - 1, j

        if j < len(data[i]) - 1:
            yield i - 1, j + 1

    # same row
    if j > 0:
        yield i, j - 1

    if j < len(data[i]) - 1:
        yield i, j + 1

    # row below
    if i < len(data) - 1:
        if j > 0:
            yield i + 1, j - 1

        yield i + 1, j

        if j < len(data[i]) - 1:
            yield i + 1, j + 1


def part2(data):
    gears = []

    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char == "*" and not char.isdigit():
                numbers_touching_cnt = 0

                prev = -99, -99

                for ni, nj in neighbors(i, j, data):
                    if data[ni][nj].isdigit():
                        # prevent double counting
                        if (
                            prev[0] != ni
                            or prev[1] != nj - 1
                            or not data[prev[0]][prev[1]].isdigit()
                        ):
                            numbers_touching_cnt += 1

                    prev = ni, nj

                if numbers_touching_cnt == 2:
                    gears.append((i, j))

    print(gears)

    res = 0

    for i, j in gears:
        used = [["." for _ in range(len(data[0]))] for _ in range(len(data))]

        numbers = []

        for ni, nj in neighbors(i, j, data):
            if data[ni][nj].isdigit() and used[ni][nj] != 1:
                number = ""

                while nj > 0 and data[ni][nj - 1].isdigit():
                    nj -= 1

                number += data[ni][nj]
                used[ni][nj] = 1

                while nj < len(data[ni]) - 1 and data[ni][nj + 1].isdigit():
                    nj += 1
                    number += data[ni][nj]
                    used[ni][nj] = 1

                numbers.append(int(number))

        if numbers:
            res += numbers[0] * numbers[1]

    return res


def test_func():
    full = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    # assert part1(full.split("\n")) == 4361
    assert part2(full.split("\n")) == 467835
