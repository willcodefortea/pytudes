from typing import Sequence

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
    total = 0
    position = 50

    for goes_right, amount in data:
        mul = 1 if goes_right else -1
        new_position = position + amount * mul

        # clamp position, i.e. -13 becomes 87
        position = new_position % 100
        # and then where did we end up
        total += position == 0

    return total


def part_2(data: Data):
    total = 0
    position = 50

    for goes_right, amount in data:
        mul = 1 if goes_right else -1
        new_position = position + amount * mul

        # how many times are we fully rotating the dial?
        complete_rotations = abs(new_position) // 100
        total += complete_rotations

        # did it cross zero or land at zero?
        total += position > 0 and new_position <= 0
        position = new_position % 100

    return total


SOLUTION = aoc.Solution(
    day=1,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=1132,
    part_2_answer=6623,
)
