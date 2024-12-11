"""
Day 5: Print Queue

This one was pretty quick. As we are always summing the middle number the
sorting direction is irrelevant, making the second stage slightly less fiddly.
"""

import re
from collections import defaultdict
from functools import cmp_to_key
from typing import NamedTuple, Sequence

import aoc

Rules = dict[int, set[int]]
Update = list[int]
Data = NamedTuple("Data", (("rules", Rules), ("updates", list[Update])))


def parse_input(lines: Sequence[str]) -> Data:
    rules: dict[int, set[int]] = defaultdict(set)
    updates: list[list[int]] = []

    lines_itr = iter(lines)
    for rule in lines_itr:
        if not rule:
            break
        left, right = rule.split("|")
        rules[int(left)].add(int(right))

    for update in lines_itr:
        if not update:
            continue
        nums = re.findall(r"\d+", update)
        updates.append([int(n) for n in nums])

    return Data(rules=rules, updates=updates)


def part_1(data: Data):
    good_updates = [u for u in data.updates if _is_valid_order(data.rules, u)]
    return _sum_middle(good_updates)


def part_2(data: Data):
    bad_updates = [u for u in data.updates if not _is_valid_order(data.rules, u)]
    fixed_updates = [_fix_update(data.rules, u) for u in bad_updates]
    return _sum_middle(fixed_updates)


def _sum_middle(updates: list[Update]):
    return sum(update[int(len(update) / 2)] for update in updates)


def _is_valid_order(rules: Rules, update: Update):
    printed = set()

    for num in update:
        printed.add(num)

        if num not in rules:
            continue

        if rules[num] & printed:
            return False

    return True


def _fix_update(rules: Rules, update: Update):
    def cmp(a: int, b: int):
        if a in rules and b in rules[a]:
            return -1
        return 1

    new_update = sorted(update, key=cmp_to_key(cmp))
    return new_update


SOLUTION = aoc.Solution(
    day=5,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=5948,
    part_2_answer=3062,
)


def test_part_1():
    data = parse_input(TEST_DATA)
    assert part_1(data) == 143


def test_part_2():
    data = parse_input(TEST_DATA)
    assert part_2(data) == 123


TEST_DATA = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""".split(
    "\n"
)
