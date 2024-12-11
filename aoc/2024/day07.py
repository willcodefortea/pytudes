"""
Day 7: Bridge Repair

Enjoyed this one, a quick depth-first-search to explore the different
combinations was easily extendable for part 2.

Python's operator module comes in handy for things like this.

** UPDATE **

After doing some research I saw that this problem can be thought of in terms of
an optimised sub-problem. As we need all operations from left-to-right to be
correct, we can reduce our search space by going backwards.


Say we had this example path:

X = a + b * c

This can only be the case if X is divisible by c. If it isn't, then it can't
possibly by a solution, so we can discard the path.

This approach takes the runtime from 1.4s to 0.03. 

Nice.
"""

import operator
import re
from math import log10
from typing import Callable, Sequence

import aoc

Op = Callable[[int, int], int]
Data = list[list[int]]


def parse_input(lines: Sequence[str]) -> Data:
    results: Data = []
    for line in lines:
        if not line:
            continue
        nums = re.findall(r"\d+", line)
        results.append(list(map(int, nums)))
    return results


def part_1(data: Data):
    return _sum_valid(data, [operator.sub, operator.truediv])


def part_2(data: Data):
    return _sum_valid(data, [operator.sub, operator.truediv, _unconcat])


def _sum_valid(data: Data, operations: list[Op]):
    total = 0
    for target, *nums in data:
        if _can_compute(target, nums, operations):
            total += target
    return total


def _can_compute(target: int, nums: list[int], operations: list[Op]) -> bool:

    def optimised_sub_problem(carry: int | float, remaining: list[int]):
        if carry % 1 or not remaining:
            return False

        carry = int(carry)
        *head, tail = remaining

        is_complete = carry == tail and len(head) == 0
        return is_complete or any(
            optimised_sub_problem(op(carry, tail), head) for op in operations
        )

    return optimised_sub_problem(carry=target, remaining=nums)


def _unconcat(a: int, b: int) -> float:
    return (a - b) / (10 ** int(log10(b) + 1))


TEST_INPUT = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""".split(
    "\n"
)


def test_part_1():
    data = parse_input(TEST_INPUT)
    assert part_1(data) == 3749


def test_part_2():
    data = parse_input(TEST_INPUT)
    assert part_2(data) == 11387


SOLUTION = aoc.Solution(
    day=7,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=1298103531759,
    part_2_answer=140575048428831,
)
