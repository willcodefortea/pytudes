"""
Day 13: Claw Contraption

We're solving for:

x * A + y * B = C

But it's a vector, so actually we have
        ┌     ┐   ┌  ┐
 ┌   ┐  │a1 b1│   │c1│
 │x y│  │     │ = │  │
 └   ┘  │a2 b2│   │c2│
        └     ┘   └  ┘
Haven't inverted a matrix for about 15 years, but we want to do
               ┌       ┐ ┌  ┐
      1        │ b2 -b1│ │c1│
─────────────  │       │ │  │
a1*b2 - b1*a2  │-a2  a1│ │c2│
               └       ┘ └  ┘
If this resolves to a ints then we have a valid solution! \o/
"""

import re
from typing import NamedTuple, Sequence

import aoc

Point = NamedTuple("Point", (("x", int), ("y", int)))
Delta = NamedTuple("Delta", (("dx", int), ("dy", int)))
Inputs = NamedTuple("Inputs", (("a", Delta), ("b", Delta), ("c", Point)))
Data = list[Inputs]


def parse_input(lines: Sequence[str]) -> Data:
    res: Data = []

    lines_iter = iter(lines)
    try:
        while True:
            a = next(lines_iter)
            b = next(lines_iter)
            prize = next(lines_iter)

            a_dx, a_dy = re.findall(r"\d+", a)
            b_dx, b_dy = re.findall(r"\d+", b)
            prize_x, prize_y = re.findall(r"\d+", prize)

            res.append(
                Inputs(
                    a=Delta(dx=int(a_dx), dy=int(a_dy)),
                    b=Delta(dx=int(b_dx), dy=int(b_dy)),
                    c=Point(x=int(prize_x), y=int(prize_y)),
                )
            )

            # skip an empty line
            next(lines_iter)
    except StopIteration:
        pass
    return res


def part_1(data: Data):
    return sum(_minimal_cost(i) for i in data)


def part_2(data: Data):
    data = [
        Inputs(
            a=d.a,
            b=d.b,
            c=Point(
                x=d.c.x + 10000000000000,
                y=d.c.y + 10000000000000,
            ),
        )
        for d in data
    ]
    return sum(_minimal_cost(i) for i in data)


def _minimal_cost(inputs: Inputs):
    a_dx, a_dy = inputs.a
    b_dx, b_dy = inputs.b

    determinant = a_dx * b_dy - a_dy * b_dx
    if determinant == 0:
        return 0

    px, py = inputs.c
    x = (b_dy * px - b_dx * py) / determinant
    y = (-a_dy * px + a_dx * py) / determinant

    if x % 1 or y % 1:
        # one or both not ints
        return 0

    return int(3 * x + y)


SOLUTION = aoc.Solution(
    day=13,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=28262,
    part_2_answer=101406661266314,
)


def test_min_cost():
    assert (
        _minimal_cost(
            inputs=Inputs(
                a=Delta(dx=94, dy=34), b=Delta(dx=22, dy=67), c=Point(x=8400, y=5400)
            )
        )
        == 280
    )


def test_part_1():
    test_input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_1(data) == 480
