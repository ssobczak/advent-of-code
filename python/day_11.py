import math
from collections import deque
from typing import Iterable, List

from utils import read_file


class Operation:
    def __init__(self, lhs: str, op: str, rhs: str):
        self._lhs = lhs
        self._op = op
        self._rhs = rhs

    @staticmethod
    def parse(description: str):
        equation = description.split("=")[1].strip()
        return Operation(*equation.split(" "))

    @staticmethod
    def _get_value(value, old):
        if value == "old":
            return old
        else:
            return int(value)

    def _apply_op(self, lhs, rhs):
        if self._op == "+":
            return lhs + rhs
        elif self._op == "*":
            return lhs * rhs
        else:
            raise ValueError(f"Unknown operator {self._op}")

    def call(self, old):
        lhs = self._get_value(self._lhs, old)
        rhs = self._get_value(self._rhs, old)
        return self._apply_op(lhs, rhs)


def test_parse_operation():
    assert Operation.parse("old = old + 2").call(5) == 7
    assert Operation.parse("old = 1 + 2").call(5) == 3
    assert Operation.parse("old = old * old").call(5) == 25


class ThrowSpec:
    def __init__(self, divisible_by, monkey_if_true, monkey_if_false):
        self.divisible_by = divisible_by
        self.monkey_if_true = monkey_if_true
        self.monkey_if_false = monkey_if_false

    @staticmethod
    def parse(test_desc, true_line, false_line):
        divisible_by = int(test_desc.split(" ")[-1])
        monkey_if_true = int(true_line.split(" ")[-1])
        monkey_if_false = int(false_line.split(" ")[-1])
        return ThrowSpec(divisible_by, monkey_if_true, monkey_if_false)

    def get_monkey(self, value):
        if value % self.divisible_by == 0:
            return self.monkey_if_true
        else:
            return self.monkey_if_false


def test_throw_spec():
    spec = ThrowSpec.parse(
        "  Test: divisible by 13",
        "       If true: throw to monkey 1",
        "       If false: throw to monkey 3",
    )
    assert spec.get_monkey(26) == 1
    assert spec.get_monkey(1) == 3


class Maupa:
    def __init__(
        self,
        group: "MonkeyGroup",
        items: Iterable[int],
        inspect: Operation,
        throw_spec: ThrowSpec,
        is_calm: bool,
    ):
        self.group = group
        self.items = deque(items)
        self.inspect = inspect
        self.throw_spec = throw_spec
        self.is_calm = is_calm

        self.inspect_cnt = 0

    def round(self):
        while self.items:
            item = self.items.popleft()
            score = self.inspect.call(item)

            if self.is_calm:
                score //= 3

            score %= self.group.modulo_factor()

            self.inspect_cnt += 1
            pass_to = self.throw_spec.get_monkey(score)
            self.group.pass_item(pass_to, score)

    def take_item(self, item):
        self.items.append(item)


class MonkeyGroup:
    def __init__(self, is_calm):
        self.is_calm = is_calm
        self.monkeys: List[Maupa] = []

    def pass_item(self, monkey, item):
        self.monkeys[monkey].take_item(item)

    def round(self):
        for monkey in self.monkeys:
            monkey.round()

    def modulo_factor(self):
        return math.prod(monkey.throw_spec.divisible_by for monkey in self.monkeys)

    def print_group(self):
        for i, monkey in enumerate(self.monkeys):
            print(f"Monkey {i}: {monkey.items}")

    def print_inspected(self):
        for i, monkey in enumerate(self.monkeys):
            print(f"Monkey {i} inspected items {monkey.inspect_cnt} times.")

    def read(self, lines):
        while next(lines, "").startswith("Monkey"):
            int_list = next(lines).split(":")[1]
            items = map(int, int_list.split(","))

            operation = Operation.parse(next(lines).split(":")[1])
            throw_spec = ThrowSpec.parse(next(lines), next(lines), next(lines))

            self.monkeys.append(Maupa(self, items, operation, throw_spec, self.is_calm))

            next(lines, "")  # skip empty line

    def most_active_score(self):
        scores = sorted(self.monkeys, key=lambda m: m.inspect_cnt, reverse=True)
        return scores[0].inspect_cnt * scores[1].inspect_cnt


def score_after_rounds(lines, rounds, is_calm=True, debug=False):
    group = MonkeyGroup(is_calm)
    group.read(lines)

    for i in range(1, rounds + 1):
        group.round()

        if debug:
            if i % 1000 == 0:
                print(f"\n== After round {i} ==")
                group.print_inspected()

    return group.most_active_score()


TEST_DATA = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".splitlines()


def test_modulo_factor():
    group = MonkeyGroup(is_calm=True)
    group.read(iter(TEST_DATA))

    assert group.modulo_factor() == 23 * 19 * 13 * 17


def test_calm():
    assert score_after_rounds(iter(TEST_DATA), rounds=20) == 10605

    big_input = read_file("../inputs/day_11.txt", skip_empty=False)
    assert score_after_rounds(big_input, rounds=20) == 66802


def test_not_calm():
    assert (
        score_after_rounds(iter(TEST_DATA), rounds=10_000, is_calm=False, debug=True)
        == 2713310158
    )

    big_input = read_file("../inputs/day_11.txt", skip_empty=False)
    assert score_after_rounds(big_input, rounds=10_000, is_calm=False) == 21800916620
