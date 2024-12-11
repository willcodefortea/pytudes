"""
Day 6: Guard Gallivant

I quite enjoy using complex numbers to represent position and heading, it makes
performing rotations really simple.

Part 2 currently runs quite slowly as there's lots of duplicate work being done,
and there's probably a more efficient way of knowing when you'll hit an
obstacle.

Might come back to this one!

UPDATE

Saved a few seconds by using a dict instead of a list of lists and indexing
positions using a complex so there's no type conversions.

Sure there's a faster way of walking / storing the paths, but I can't see one
right now.
"""

from typing import Sequence

import aoc

Grid = dict[complex, str]
Data = tuple[Grid, complex]


def parse_input(lines: Sequence[str]) -> Data:
    start = None
    grid: Grid = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            pos = complex(x, y)
            grid[pos] = char

            if char == "^":
                start = pos

    assert start
    return grid, start


def part_1(data: Data):
    grid, start = data
    route, _ = _explore_path(grid, start)
    return len(set(point for point, _ in route))


def part_2(data: Data):
    grid, start = data
    current_route, _ = _explore_path(grid, start)

    # now we have the path, try adding an obstacle at each point
    # other the first
    possible_obstructions = set([p for p, _ in current_route if p != start])
    loops = 0

    for point in possible_obstructions:
        grid[point] = "#"
        _, looped = _explore_path(grid, start)
        loops += int(looped)
        grid[point] = "."

    return loops


SOLUTION = aoc.Solution(
    day=6,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=4973,
    part_2_answer=1482,
)


def _explore_path(data: Grid, guard_position: complex):
    heading = -1j
    visited = set([(guard_position, heading)])
    looped = False

    while True:
        next_position = guard_position + heading

        try:
            if data[next_position] == "#":
                # rotate right
                heading *= 1j
                continue
        except KeyError:
            # out of bounds
            break

        if (next_position, heading) in visited:
            looped = True
            break

        guard_position = next_position
        visited.add((guard_position, heading))

    return visited, looped


TEST_INPUT = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""".split(
    "\n"
)


def test_part_1():
    data = parse_input(TEST_INPUT)
    assert part_1(data) == 41


def test_part_2():
    data = parse_input(TEST_INPUT)
    assert part_2(data) == 6


def test_part_2_limits():
    assert SOLUTION.part_2() < 1656
