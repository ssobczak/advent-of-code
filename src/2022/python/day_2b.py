import os
from enum import Enum

from src.helpers import read_file


class FigureType(Enum):
    ROCK = "ROCK"
    PAPER = "PAPER"
    SCISSORS = "SCISSORS"

    @classmethod
    def from_letter(cls, letter: str):
        if letter == "A":
            return cls.ROCK
        elif letter == "B":
            return cls.PAPER
        elif letter == "C":
            return cls.SCISSORS


class Outcome(Enum):
    WIN = "WIN"
    DRAW = "DRAW"
    LOSS = "LOSS"

    @classmethod
    def from_letter(cls, letter: str):
        if letter == "X":
            return cls.LOSS
        elif letter == "Y":
            return cls.DRAW
        elif letter == "Z":
            return cls.WIN


class GameRules:
    WINNING_ORDER = [FigureType.ROCK, FigureType.PAPER, FigureType.SCISSORS]

    def __init__(self, figure_type: FigureType):
        self.figure_type = figure_type

    def wins_with(self) -> FigureType:
        idx = self.WINNING_ORDER.index(self.figure_type)
        return self.WINNING_ORDER[(idx + 1) % len(self.WINNING_ORDER)]

    def loses_with(self) -> FigureType:
        idx = self.WINNING_ORDER.index(self.figure_type)
        return self.WINNING_ORDER[(idx - 1) % len(self.WINNING_ORDER)]


class Position:
    OUTCOME_SCORES = {
        Outcome.WIN: 6,
        Outcome.DRAW: 3,
        Outcome.LOSS: 0,
    }

    FIGURE_SCORES = {
        FigureType.ROCK: 1,
        FigureType.PAPER: 2,
        FigureType.SCISSORS: 3,
    }

    def __init__(self, opponent: FigureType, outcome: Outcome):
        self.opponent = opponent
        self.outcome = outcome

    def score(self):
        my_move = self.get_my_move()
        return self.OUTCOME_SCORES[self.outcome] + self.FIGURE_SCORES[my_move]

    def get_my_move(self) -> FigureType:
        game = GameRules(self.opponent)

        if self.outcome == Outcome.WIN:
            return game.wins_with()
        elif self.outcome == Outcome.DRAW:
            return game.figure_type
        else:
            return game.loses_with()

    def __str__(self):
        return (
            f"Opponent: {self.opponent}, for outcome {self.outcome} "
            f"I play {self.get_my_move()} and score {self.score()} pts."
        )


def calculate_score(input_data, debug=False):
    total_score = 0

    for row in input_data:
        me = FigureType.from_letter(row.split(" ")[0])
        outcome = Outcome.from_letter(row.split(" ")[1])

        position = Position(me, outcome)
        if debug:
            print(position)

        total_score += position.score()

    return total_score


def test_calculate_score():
    assert calculate_score("A Y\nB X\nC Z".split("\n")) == 12
    assert (
        calculate_score(read_file(os.path.dirname(__file__) + "/../inputs/day_2.txt"))
        == 13490
    )
