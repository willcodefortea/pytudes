"""
Day 11: Plutonian Pebbles

I went a very different route initially, using a deque
to store the stones and tracking them all, rotating the
deque so always working at the head.

This was fine for part 1 but as the number of stones grows
exponentially, part 2 quickly becomes incomputable. I tried
finding the coefficients for the growth, but it was not
static, so needed another approach.

As each stone is independent, we don't actually need to 
keep track of the whole list. All we care about is for any
given stone, how many times will it split in N steps?

Then all that's needed is some memoization via functools'
cache decorator and voila, no duplicate work and a speedy
answer!
"""

import re
from typing import Sequence
from math import log10
from functools import cache

import aoc

Data = list[int]


def parse_input(lines: Sequence[str]) -> Data:
    return list(int(c) for c in re.findall(r"\d+", lines[0]))


def part_1(data: Data):
    res = sum(_count_splits(x, 25) for x in data)
    return res


def part_2(data: Data):
    res = sum(_count_splits(x, 75) for x in data)
    return res


@cache
def _count_splits(num: int, steps: int):
    if steps == 0:
        # no more splits, so only 1 number!
        return 1

    # rule 1
    if num == 0:
        return _count_splits(1, steps - 1)

    # rule 2
    num_digits = int(log10(num)) + 1
    if num_digits % 2 == 0:
        lhs = num // 10 ** (num_digits // 2)
        rhs = num % 10 ** (num_digits // 2)

        return _count_splits(lhs, steps - 1) + _count_splits(rhs, steps - 1)

    # rule 3
    return _count_splits(num * 2024, steps - 1)


SOLUTION = aoc.Solution(
    day=11,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=198075,
    part_2_answer=235571309320764,
)


def test_part_1():
    stones = list([125, 17])
    assert part_1(stones) == 55312
