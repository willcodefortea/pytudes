from typing import Sequence
import aoc

Data = Sequence[str]


def parse_input(lines: Sequence[str]) -> Data:
    return lines


def part_1(data: Data): ...


def part_2(data: Data): ...


SOLUTION = aoc.Solution(
    day=1,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=-1,
    part_2_answer=-1,
)
