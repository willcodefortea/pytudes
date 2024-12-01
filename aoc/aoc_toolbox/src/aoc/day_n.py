import aoc

Data = list[str]


def parse_input(lines: list[str]) -> Data:
    return lines


def part_1(data: Data): ...


def part_2(data: Data): ...


SOLUTION = aoc.Solution(
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=-1,
    part_2_answer=-1,
)
