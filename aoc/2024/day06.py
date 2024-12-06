from typing import NamedTuple, Sequence

import aoc

Grid = list[list[str]]
Data = tuple[Grid, complex]


def parse_input(lines: Sequence[str]) -> Data:
    grid = [list(line) for line in lines if line]

    start = None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "^":
                start = complex(x, y)

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
    possible_obstructions = set([p for p, _ in current_route]) - set([start])
    loops = 0

    for point in possible_obstructions:
        ox, oy = int(point.real), int(point.imag)
        grid[oy][ox] = "#"
        _, looped = _explore_path(grid, start)
        loops += int(looped)
        grid[oy][ox] = "."

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
        nx = int(next_position.real)
        ny = int(next_position.imag)
        within_bounds = 0 <= nx < len(data[0]) and 0 <= ny < len(data)

        if not within_bounds:
            break

        if data[ny][nx] == "#":
            # rotate right
            heading *= 1j
            continue

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
