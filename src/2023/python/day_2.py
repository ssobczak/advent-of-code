class Throw:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    @classmethod
    def parse(cls, description: str) -> "Throw":
        red, green, blue = 0, 0, 0

        for dc in description.split(", "):
            number, color = dc.split(" ")
            if color == "red":
                red = int(number)
            if color == "green":
                green = int(number)
            if color == "blue":
                blue = int(number)

        return cls(red, green, blue)

    def is_real(self):
        return self.red < 12 and self.green < 13 and self.blue < 14


class Game:
    def __init__(self, number: int, throws: list[Throw]):
        self.number = number
        self.throws = throws

    @classmethod
    def parse(cls, description: str) -> "Game":
        game, dice = description.split(": ")
        _, game_no = game.split(" ")

        throws = [Throw.parse(throw) for throw in dice.split("; ")]

        return cls(int(game_no), throws)

    def is_real(self):
        return all(t.is_real() for t in self.throws)

    def power(self):
        red = max(t.red for t in self.throws)
        green = max(t.green for t in self.throws)
        blue = max(t.blue for t in self.throws)

        return red * green * blue


def func(data):
    res1, res2 = 0, 0

    for line in data.split("\n"):
        game = Game.parse(line)

        if game.is_real():
            res1 += int(game.number)

        res2 += game.power()

    return res1, res2


def test_func():
    data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    assert func(data) == (8, 2286)
