"""
Day 19: Linen Layout

Using the cache decorator here made it very simple to solve this problem but it
feels like a bit of a cheat!

As a whole this feels like some kind of dynamic programming, coin-change
problem, so I may come back and explore what that solution would look like.
"""

import re
from functools import cache
from typing import NamedTuple, Sequence

import aoc


Data = NamedTuple("Data", (("towels", tuple[str]), ("patterns", tuple[str, ...])))


def parse_input(lines: Sequence[str]) -> Data:
    towels = tuple(re.findall(r"\w+", lines[0]))
    patterns = tuple(line for line in lines[2:] if line)
    return Data(towels=towels, patterns=patterns)


def part_1(data: Data):
    return len([p for p in data.patterns if can_create_pattern(p, data.towels)])


@cache
def can_create_pattern(pattern: str, towels: tuple[str]):
    if len(pattern) == 0:
        return 1

    num_successful = 0
    for towel in towels:
        if pattern.startswith(towel):
            num_successful += can_create_pattern(pattern[len(towel) :], towels)

    return num_successful


def part_2(data: Data):
    return sum(can_create_pattern(p, data.towels) for p in data.patterns)


SOLUTION = aoc.Solution(
    day=19,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=-1,
    part_2_answer=-1,
)


def test_part_1():
    test_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_1(data) == 6


def test_part_2():
    test_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_2(data) == 16
