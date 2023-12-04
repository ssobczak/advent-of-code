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


class Rucksack:
    def __init__(self, line: str):
        comp_size = int(len(line) / 2)
        self.left_comp = set(line[:comp_size])
        self.right_comp = set(line[comp_size:])

    def get_item_in_both(self):
        return self.left_comp.intersection(self.right_comp)

    def score(self):
        item_in_both = self.get_item_in_both().pop()
        return SCORES[item_in_both]


def test_rucksack():
    assert Rucksack("ab").left_comp == set("a")
    assert Rucksack("ab").right_comp == set("b")


def test_get_item_in_both():
    assert Rucksack("qwease").get_item_in_both() == set("e")
    assert Rucksack("vJrwpWtwJgWrhcsFMMfFFhFp").get_item_in_both() == set("p")


def calculate_score(input_lines):
    return sum(Rucksack(line).score() for line in input_lines)


def test_calculate_score():
    example = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

    assert calculate_score(example.split("\n")) == 157
    assert (
        calculate_score(read_file(os.path.dirname(__file__) + "/../inputs/day_3.txt"))
        == 7903
    )
