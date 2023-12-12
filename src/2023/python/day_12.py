import os
from functools import lru_cache

from src.helpers import read_file


@lru_cache(maxsize=1_000_000)
def combinations(symbols, numbers):
    symbols = symbols.strip(".")

    if len(numbers) == 0:
        if any(s == "#" for s in symbols):
            return 0
        else:
            return 1

    for i in range(len(symbols)):
        if symbols[i] == ".":
            num = sum(1 for s in symbols[:i] if s == "#")
            if num == numbers[0]:
                return combinations(symbols[i + 1 :], numbers[1:])
            else:
                return 0

        if symbols[i] == "#":
            continue

        if symbols[i] == "?":
            return combinations(symbols[:i] + "#" + symbols[i + 1 :], numbers) + combinations(
                symbols[:i] + "." + symbols[i + 1 :], numbers
            )

    if len(numbers) == 1 and sum(1 for s in symbols if s == "#") == numbers[0]:
        return 1

    return 0


def part1(data):
    res = 0

    for line in data:
        symbols, nums = line.split()
        numbers = tuple(int(n) for n in nums.split(","))
        c = combinations(symbols, numbers)
        res += c

    return res


def part2(data):
    res = 0
    for line in data:
        symbols, nums = line.split()
        numbers = [int(n) for n in nums.split(",")]

        long_symbols = symbols + "?" + symbols + "?" + symbols + "?" + symbols + "?" + symbols
        long_numbers = numbers + numbers + numbers + numbers + numbers

        c = combinations(long_symbols, tuple(long_numbers))
        res += c

    return res


EXAMPLE = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def test_part1():
    assert part1(["???.### 1,1,3"]) == 1
    assert part1([".??..??...?##. 1,1,3"]) == 4
    assert part1(["?#?#?#?#?#?#?#? 1,3,1,6"]) == 1
    assert part1(["????.#...#... 4,1,1"]) == 1
    assert part1(["????.######..#####. 1,6,5"]) == 4
    assert part1(["?###???????? 3,2,1"]) == 10
    assert part1(["#?.?#????????#???? 1,1,3"]) == 3

    assert part1(EXAMPLE.splitlines(keepends=False)) == 21
    input = read_file(os.path.dirname(__file__) + "/../inputs/day_12.txt")
    assert part1(input) == 7622


def test_part2():
    assert part2(["????#?#???.??.. 9,2"]) == 162
    assert part2(["?.#?????????###.?# 1,1,2,1,5,1"]) == 243
    assert part2([".???#????#?????#?#? 1,9,4"]) == 76896
    assert part2(["?#?.??.#?.??? 2,1,1,1"]) == 2778836
    assert part2(["?????????#?###???.?. 1,9"]) == 24598156

    assert part2(EXAMPLE.splitlines(keepends=False)) == 525152
    input = read_file(os.path.dirname(__file__) + "/../inputs/day_12.txt")
    assert part2(input) == 4964259839627
