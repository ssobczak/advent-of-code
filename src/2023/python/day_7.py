import os
from collections import Counter
from enum import Enum
from functools import cached_property
from typing import Tuple, List

from src.helpers import read_file

INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

card_strength = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
card_strength_map = {card: i + 2 for i, card in enumerate(reversed(card_strength))}


class HandStrength(Enum):
    FIVE_KIND = 7
    FOUR_KIND = 6
    FULL_HOUSE = 5
    THREE_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class Hand:
    def __init__(self, cards, j_replacement="J"):
        self.cards = cards
        self.j_replacement = j_replacement

    @cached_property
    def counts(self) -> List[Tuple[int, str]]:
        to_figure = self.cards.replace("J", self.j_replacement)
        cnts = Counter(c for c in to_figure)
        return sorted([(cnt, card) for card, cnt in cnts.items()], reverse=True)

    def card_strengths(self) -> List[int]:
        return [card_strength_map[card] for cnt, card in self.counts]

    def strength(self):
        return self.hand_type.value, [card_strength_map[card] for card in self.cards]

    @cached_property
    def hand_type(self):
        if self.counts[0][0] == 5:
            return HandStrength.FIVE_KIND
        elif self.counts[0][0] == 4:
            return HandStrength.FOUR_KIND
        elif self.counts[0][0] == 3:
            if self.counts[1][0] == 2:
                return HandStrength.FULL_HOUSE
            else:
                return HandStrength.THREE_KIND
        elif self.counts[0][0] == 2:
            if self.counts[1][0] == 2:
                return HandStrength.TWO_PAIR
            else:
                return HandStrength.ONE_PAIR
        else:
            return HandStrength.HIGH_CARD

    def optimized_J(self):
        if "J" not in self.cards:
            return self

        best_hand = self

        for replacement in card_strength[:-1]:
            new_hand = Hand(self.cards, replacement)
            if new_hand.hand_type.value > best_hand.hand_type.value:
                best_hand = new_hand

        return best_hand

    def __repr__(self):
        return f"Hand({self.cards}, J->{self.j_replacement}, {self.hand_type})"


def parse(data):
    for line in data:
        h, bet = line.split()
        yield Hand(h), int(bet)


def score(data):
    wins = sorted(data, key=lambda x: x[0].strength())

    res = 0
    for i, (h, bet) in enumerate(wins):
        print(i + 1, bet, h)
        res += bet * (i + 1)

    return res


def part1(data):
    return score(data)


def test_part1():
    td = list(parse(INPUT.splitlines(keepends=False)))
    assert part1(td) == 6440


def part2(data):
    optimized = [(h.optimized_J(), bet) for h, bet in data]
    return score(optimized)


def test_part2():
    td = parse(INPUT.splitlines(keepends=False))
    assert part2(td) == [4, 8, 9]


def test_final():
    final = read_file(os.path.dirname(__file__) + "/../inputs/day_7.txt")
    td = list(parse(final))

    print(part1(td))
    print(part2(td))
