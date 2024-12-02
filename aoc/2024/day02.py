"""
Day 2: Red-Nosed Reports

Not super happy with my soution here, it's quite messsy. I
explored using generators and advancing one to represent the
skip in part 2, but that was far more difficult to reason about
AND didn't cover all cases. The simple "just remove every index
and revealuate" proved to be far easier to follow.
"""

import re
from typing import Sequence
import aoc

Data = list[list[int]]


def parse_input(lines: Sequence[str]) -> Data:
    res: Data = []
    for line in lines:
        if m := re.findall(r"\d+", line):
            res.append([int(d) for d in m])
    return res


def part_1(data: Data):
    return len([report for report in data if _is_good_report(report)])


def part_2(data: Data):
    num_good = 0

    for report in data:
        if not _is_good_report(report):
            for i in range(len(report)):
                new_rep = report[:]
                del new_rep[i]

                if _is_good_report(new_rep):
                    num_good += 1
                    break
            continue

        num_good += 1
    return num_good


def _is_good(a: int, b: int, sign: int):
    diff = a - b
    diff_sign = -1 if diff < 0 else 1
    return 1 <= abs(diff) <= 3 and sign == diff_sign


def _is_good_report(report: list[int]):
    pairs = zip(report, report[1:])
    # are we ascending or descending?
    sign = -1 if report[0] < report[1] else 1
    for a, b in pairs:
        is_good = _is_good(a, b, sign)
        if not is_good:
            return False
    return True


TEST_DATA = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""".split(
    "\n"
)


def test_part_1():
    test_data = parse_input(TEST_DATA)
    assert part_1(test_data) == 2


def test_part_2():
    test_data = parse_input(TEST_DATA)
    assert part_2(test_data) == 4, "Bad test 2"


SOLUTION = aoc.Solution(
    day=2,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=534,
    part_2_answer=577,
)
