import re
from typing import Literal, Sequence

import aoc

Op = Literal["mul", "do", "dont"]
Data = Sequence[tuple[Op, int, int]]


def parse_input(lines: Sequence[str]) -> Data:
    pairs: Data = []
    for line in lines:
        valid_ops = re.findall(r"mul\(\d+,\d+\)|don't\(\)|do\(\)", line)
        for op in valid_ops:
            if op.startswith("mul"):
                a, b = op[4:-1].split(",")
                pairs.append(("mul", int(a), int(b)))
            elif op.startswith("don't"):
                pairs.append(("dont", 0, 0))
            elif op.startswith("do"):
                pairs.append(("do", 0, 0))
    return pairs


def part_1(data: Data):
    return sum(a * b for o, a, b in data if o == "mul")


def part_2(data: Data):
    apply = True
    res = 0
    for op, a, b in data:
        if op == "mul" and apply:
            res += a * b
        if op == "do":
            apply = True
        if op == "dont":
            apply = False
    return res


SOLUTION = aoc.Solution(
    day=3,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=159833790,
    part_2_answer=89349241,
)


def test_part_1_with_sample():
    data = parse_input(
        """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))""".split(
            "\n"
        )
    )
    assert part_1(data) == 161


def test_part_2_with_samle():
    data = parse_input(
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))".split(
            "\n"
        )
    )
    assert part_2(data) == 48
