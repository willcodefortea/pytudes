import re
from collections import Counter

import aoc

Data = tuple[list[int], list[int]]


def parse_input(lines: list[str]) -> Data:
    left, right = [], []
    for line in lines:
        if m := re.match(r"(\d+)\s+(\d+)", line):
            l, r = m.groups()
            left.append(int(l))
            right.append(int(r))
    return left, right


def part_1(data: Data):
    left, right = data
    return sum(abs(l - r) for l, r in zip(sorted(left), sorted(right)))


def part_2(data: Data):
    left, right = data
    right_counts = Counter(right)
    return sum(l * right_counts.get(l, 0) for l in set(left))


SOLUTION = aoc.Solution(
    day=1,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=1222801,
    part_2_answer=22545250,
)
