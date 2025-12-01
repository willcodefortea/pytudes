from typing import Sequence
from collections import deque

import aoc

Data = Sequence[tuple[bool, int]]


def parse_input(lines: Sequence[str]) -> Data:
    results = []
    for line in lines:
        if not line:
            continue
        dir, num = line[0], line[1:]
        results.append((dir == "R", int(num)))

    return results


def part_1(data: Data):
    dial = deque(range(100))
    dial.rotate(50)
    total = 0

    for goes_right, amount in data:
        if not goes_right:
            amount = amount * -1

        dial.rotate(amount)
        if dial[0] == 0:
            total += 1
    return total


def part_2(data: Data):
    dial = deque(range(100))
    dial.rotate(50)
    total = 0

    for goes_right, amount in data:
        dir = 1
        if not goes_right:
            dir = -1

        for _ in range(amount):
            dial.rotate(dir)
            if dial[0] == 0:
                total += 1

    return total


SOLUTION = aoc.Solution(
    day=1,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=1132,
    part_2_answer=6623,
)
