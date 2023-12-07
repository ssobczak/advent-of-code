import os
from collections import Counter
from enum import Enum
from functools import cached_property
from typing import Tuple, List

from src.helpers import read_file

SAMPLE_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


class HandStrength(Enum):
    FIVE_KIND = 7
    FOUR_KIND = 6
    FULL_HOUSE = 5
    THREE_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class CardStrength:
    def __init__(self, j_lowest):
        self.j_lowest = j_lowest

    @cached_property
    def order(self):
        if self.j_lowest:
            return ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
        else:
            return ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    @cached_property
    def strength_map(self):
        return {card: i + 2 for i, card in enumerate(reversed(self.order))}

    def get(self, card):
        return self.strength_map[card]


class Hand:
    def __init__(self, cards, card_strength: CardStrength, j_replacement="J"):
        self.cards = cards
        self.j_replacement = j_replacement
        self.card_strength = card_strength

    @cached_property
    def counts(self) -> List[Tuple[int, str]]:
        to_figure = self.cards.replace("J", self.j_replacement)
        cnts = Counter(c for c in to_figure)
        return sorted([(cnt, card) for card, cnt in cnts.items()], reverse=True)

    @cached_property
    def card_strengths(self) -> List[int]:
        return [self.card_strength.get(card) for card in self.cards]

    def strength(self):
        return self.hand_type.value, self.card_strengths

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

    def optimized_j(self):
        if "J" not in self.cards:
            return self

        best_hand = self

        for j_replacement in self.cards.replace("J", ""):
            new_hand = Hand(self.cards, self.card_strength, j_replacement)
            if new_hand.hand_type.value > best_hand.hand_type.value:
                best_hand = new_hand

        return best_hand

    def __repr__(self):
        return f"Hand({self.cards}, J->{self.j_replacement}, {self.hand_type})"


def parse(data, card_strength_map):
    for line in data:
        h, bet = line.split()
        yield Hand(h, card_strength_map), int(bet)


def score(data):
    wins = sorted(data, key=lambda x: x[0].strength())

    res = 0
    for i, (h, bet) in enumerate(wins):
        # print(i + 1, bet, h)
        res += bet * (i + 1)

    return res


def part1(data):
    card_strength = CardStrength(j_lowest=False)
    return score(parse(data, card_strength))


def test_part1():
    assert part1(SAMPLE_INPUT.splitlines(keepends=False)) == 6440


def part2(data):
    card_strength = CardStrength(j_lowest=True)
    parsed = parse(data, card_strength)
    optimized = [(h.optimized_j(), bet) for h, bet in parsed]
    return score(optimized)


def test_part2():
    assert part2(SAMPLE_INPUT.splitlines(keepends=False)) == 5905


def test_main():
    final = read_file(os.path.dirname(__file__) + "/../inputs/day_7.txt")
    assert part1(final) == 245794640

    final = read_file(os.path.dirname(__file__) + "/../inputs/day_7.txt")
    assert part2(final) == 247899149
