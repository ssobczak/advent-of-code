import math
import os

from src.helpers import read_file


def parse(data):
    instructions = data[0]

    graph = {}
    for line in data[1:]:
        node, links = line.split(" = ")
        left, right = links.strip("()").split(", ")
        graph[node] = (left, right)

    return instructions, graph


def part1(current, instructions, graph):
    i = 0
    while True:
        instruction = instructions[i % len(instructions)]
        i += 1

        if instruction == "L":
            current = graph[current][0]
        else:
            current = graph[current][1]

        if current.endswith("Z"):
            return i


def find_lcm(num1, num2):
    return (num1 * num2) // math.gcd(num1, num2)


def find_lcm_list(lst):
    num1 = lst[0]
    num2 = lst[1]
    lcm = find_lcm(num1, num2)

    for i in range(2, len(lst)):
        lcm = find_lcm(lcm, lst[i])

    return lcm


def part2(instructions, graph):
    starts = [node for node in graph.keys() if node.endswith("A")]
    steps = [part1(start, instructions, graph) for start in starts]

    print(steps)

    return find_lcm_list(steps)


def test_part1():
    sample1 = """RL
AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
    instructions, graph = parse(sample1.splitlines(keepends=False))
    assert part1("AAA", instructions, graph) == 2

    sample2 = """LLR
AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    instructions, graph = parse(sample2.splitlines(keepends=False))
    assert part1("AAA", instructions, graph) == 6

    final = list(read_file(os.path.dirname(__file__) + "/../inputs/day_8.txt"))
    assert part1("AAA", *parse(final)) == 15517


def test_part2():
    SAMPLE_INPUT = """LR
11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

    instructions, graph = parse(SAMPLE_INPUT.splitlines(keepends=False))
    assert part2(instructions, graph) == 6

    final = list(read_file(os.path.dirname(__file__) + "/../inputs/day_8.txt"))
    assert part2(*parse(final)) == 14935034899483
