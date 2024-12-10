"""
Day 10: Hoof It

I never learn to read the question! Stuck on part 1 for a
while because I wasn't looking at distinct peaks.

I thought I might need to make use of caching the DFS but
it turned out to be fast enough. Modifying the result for
part 2 was pretty straightforward, which is always a treat!
"""

from typing import DefaultDict, NamedTuple, Sequence

import aoc

Point = NamedTuple("Point", (("x", int), ("y", int)))
Grid = tuple[tuple[int]]
Data = NamedTuple("Data", (("grid", Grid), ("trailheads", list[Point])))


def parse_input(lines: Sequence[str]) -> Data:
    grid = []
    trailheads = []
    for y, line in enumerate(lines):
        if not line:
            break

        row: list[int] = []
        for x, char in enumerate(line):
            if char == ".":
                row.append(-1)
            else:
                row.append(int(char))
                if char == "0":
                    trailheads.append(Point(x, y))
        grid.append(tuple(row))

    return Data(tuple(grid), trailheads)


def part_1(data: Data):
    scores = DefaultDict(int)

    for trailhead in data.trailheads:
        reachable_peaks = _peaks_on_distinct_paths(data.grid, trailhead)
        num_distinct_peaks = len(set(reachable_peaks))
        scores[trailhead] = num_distinct_peaks

    return sum(scores.values())


def part_2(data: Data):
    scores = DefaultDict(int)

    for trailhead in data.trailheads:
        peaks = _peaks_on_distinct_paths(data.grid, trailhead)
        num_paths = len(peaks)
        scores[trailhead] = num_paths

    return sum(scores.values())


def _peaks_on_distinct_paths(grid: Grid, location: Point, target: int = 1):
    if target == 10:
        return [location]

    peaks: list[Point] = []
    for point in _neighbours(grid, location):
        x, y = point
        if grid[y][x] == target:
            peaks += _peaks_on_distinct_paths(grid, point, target=target + 1)

    return peaks


def _neighbours(grid: Sequence[Sequence[int]], point: Point):
    deltas = ((1, 0), (0, 1), (-1, 0), (0, -1))

    for dx, dy in deltas:
        nx, ny = point.x + dx, point.y + dy

        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            yield Point(x=nx, y=ny)


SOLUTION = aoc.Solution(
    day=10,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=688,
    part_2_answer=1459,
)


def test_part_1_multple_paths():
    test_input = """..90..9
...1.98
...2..7
6543456
765.987
876....
987....""".split(
        "\n"
    )
    data = parse_input(test_input)

    assert part_1(data) == 4


def test_part_1_multple_trailheads():
    test_input = """10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01""".split(
        "\n"
    )
    data = parse_input(test_input)

    assert part_1(data) == 3


def test_part_1():
    test_input = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""".split(
        "\n"
    )
    data = parse_input(test_input)

    assert part_1(data) == 36
