import re
from math import ceil, floor

from aoc import Solution


def parse_input(lines: list[str]):
    times = map(int, re.findall("\d+", lines[0]))
    distances = map(int, re.findall("\d+", lines[1]))

    return list(zip(times, distances))


def part_1(races):
    res = 1
    for time, distance in races:
        res *= num_winning_options(time, distance)

    return res


def num_winning_options(time: int, distance: int) -> int:
    # winning condition:
    # button_press * (button_press - time) > distance
    # can be rewritten as:
    # button_press ^ 2 - button_press * time - distance > 0
    # solving to find the limits gives:
    # button_press = time / 2 +- sqrt(time ^ 2 - 4 * distance) / 2
    lower = time / 2 - (time**2 - 4 * distance) ** 0.5 / 2
    upper = time / 2 + (time**2 - 4 * distance) ** 0.5 / 2

    # need integer values, so round remove the decimal part
    lower = ceil(lower)
    upper = floor(upper)
    # then add 1 to include zero \o/
    return upper - lower + 1


def part_2(races):
    times, distances = zip(*races)
    time = int("".join(str(x) for x in times))
    distance = int("".join(str(x) for x in distances))

    return num_winning_options(time, distance)


SOLUTION = Solution(
    day=6,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=608902,
    part_2_answer=46173809,
)

if __name__ == "__main__":
    print(SOLUTION.part_1(), SOLUTION.part_1_solved)
    print(SOLUTION.part_2(), SOLUTION.part_2_solved)
