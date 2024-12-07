"""
Day 7: Bridge Repair

Enjoyed this one, a quick depth-first-search to explore the
different combinations was easily extendable for part 2.

Python's operator module comes in handy for things like this.
"""

import operator
import re
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
        results.append([int(n) for n in nums])
    return results


def part_1(data: Data):
    return _sum_valid(data, [operator.add, operator.mul])


def part_2(data: Data):
    return _sum_valid(data, [operator.add, operator.mul, _concat])


def _sum_valid(data: Data, operations: list[Op]):
    total = 0
    for target, *nums in data:
        if _can_compute(target, nums, operations):
            total += target
    return total


def _can_compute(target: int, nums: list[int], operations: list[Op]) -> bool:

    def dfs(carry: int, remaining: list[int]):
        if len(remaining) == 0 or carry > target:
            return carry == target

        for op in operations:
            new_carry = op(carry, remaining[0])
            if dfs(new_carry, remaining[1:]):
                return True
        return False

    return dfs(carry=nums[0], remaining=nums[1:])


def _concat(a: int, b: int):
    return int(str(a) + str(b))


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
