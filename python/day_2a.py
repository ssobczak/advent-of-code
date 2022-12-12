from enum import Enum

from utils import read_file


class FigureType(Enum):
    ROCK = "ROCK"
    PAPER = "PAPER"
    SCISSORS = "SCISSORS"


class Figure:
    MAPPING = {
        "A": FigureType.ROCK,
        "X": FigureType.ROCK,
        "B": FigureType.PAPER,
        "Y": FigureType.PAPER,
        "C": FigureType.SCISSORS,
        "Z": FigureType.SCISSORS,
    }

    def __init__(self, letter: str):
        self.figure_type = self.MAPPING[letter]

    def is_winning_with(self, other: "Figure"):
        if self.figure_type == FigureType.ROCK:
            return other.figure_type == FigureType.SCISSORS
        elif self.figure_type == FigureType.PAPER:
            return other.figure_type == FigureType.ROCK
        elif self.figure_type == FigureType.SCISSORS:
            return other.figure_type == FigureType.PAPER


class Position:
    FIGURE_SCORES = {
        FigureType.ROCK: 1,
        FigureType.PAPER: 2,
        FigureType.SCISSORS: 3,
    }

    DRAW_SCORE = 3
    WIN_SCORE = 6

    def __init__(self, opponent: Figure, me: Figure):
        self.opponent = opponent
        self.me = me

    def score(self):
        return self.FIGURE_SCORES[self.me.figure_type] + self._game_score_part()

    def _game_score_part(self):
        if self.me.figure_type == self.opponent.figure_type:
            return self.DRAW_SCORE
        elif self.me.is_winning_with(self.opponent):
            return self.WIN_SCORE
        else:
            return 0


def total_score(data):
    total_score = 0
    for row in data:
        me, opponent = row.split(" ")
        total_score += Position(Figure(me), Figure(opponent)).score()

    return total_score


def test_total_score():
    input = """A Y
B X
C Z"""
    assert total_score(input.split("\n")) == 15
    assert total_score(read_file("../inputs/day_2.txt")) == 17189
