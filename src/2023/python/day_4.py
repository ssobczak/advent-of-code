def solution_a(data):
    res = 0

    for line in data.splitlines():
        winning, have = line.split(":")[1].split("|")

        w_num = set(int(x.strip()) for x in winning.split())
        have_num = set(int(x.strip()) for x in have.split())

        exp = len(w_num.intersection(have_num))
        if exp > 0:
            res += pow(2, exp - 1)

    return res


def solution_b(data):
    res = [1] * len(data.splitlines())

    for i, line in enumerate(data.splitlines()):
        winning, have = line.split(":")[1].split("|")

        winning_nums = set(int(x.strip()) for x in winning.split())
        have_nums = set(int(x.strip()) for x in have.split())

        exp = len(winning_nums.intersection(have_nums))
        for j in range(1, exp + 1):
            res[i + j] += res[i]

    return sum(res)


def test_example():
    data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    assert solution_a(data) == 13
    assert solution_b(data) == 30
