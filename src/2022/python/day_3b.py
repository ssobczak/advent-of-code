import os
import string
from typing import Dict

from src.helpers import read_file


def _init_scores() -> Dict[str, int]:
    res = {}

    for points, letter in enumerate(string.ascii_lowercase):
        res[letter] = points + 1

    for points, letter in enumerate(string.ascii_uppercase):
        res[letter] = points + 27

    return res


SCORES = _init_scores()


def test_scores():
    assert SCORES["a"] == 1
    assert SCORES["A"] == 27
    assert SCORES["Z"] == 52


class Group:
    def __init__(self, rucksacks: list[str]):
        self.rucksacks = [set(sack) for sack in rucksacks]

    def get_item_in_all(self) -> str:
        res = self.rucksacks[0]
        for sack in self.rucksacks[1:]:
            res = res.intersection(sack)
        return res.pop()

    def score(self):
        item_in_both = self.get_item_in_all()
        return SCORES[item_in_both]


def test_group():
    sacks = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
    ]
    assert Group(sacks).get_item_in_all() == "r"


def calculate_score(input_lines):
    score = 0
    group = []
    for line in input_lines:
        if len(group) < 3:
            group.append(line)

        if len(group) == 3:
            score += Group(group).score()
            group = []

    return score


def test_calculate_score():
    example = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

    assert calculate_score(example.split("\n")) == 70

    data = read_file(os.path.dirname(__file__) + "/../inputs/day_3.txt")
    assert calculate_score(data) == 2548
