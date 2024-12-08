"""
Day 8: Resonant Collinearity

Nothing too difficult in today's one, a little drawing
in excalidraw to make sure I was getting the points correct
and helped with TDD meant this was pretty smooth! :)
"""

from collections import defaultdict
from typing import NamedTuple, Sequence

import aoc

Point = NamedTuple("Point", (("x", int), ("y", int)))
Data = Sequence[str]


def parse_input(lines: Sequence[str]) -> Data:
    return [line for line in lines if line]


def part_1(data: Data):
    return len(_find_antinodes(data))


def part_2(data: Data):
    return len(_find_antinodes(data, all_points=True))


SOLUTION = aoc.Solution(
    day=8,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=369,
    part_2_answer=1169,
)


def _find_antinodes(data: Data, all_points: bool = False) -> set[Point]:
    antennas: dict[str, list[Point]] = defaultdict(list)

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char != ".":
                antennas[char].append(Point(x, y))

    antinodes: set[Point] = set()

    for locations in antennas.values():
        if len(locations) == 1:
            continue

        if all_points:
            for p in locations:
                antinodes.add(p)

        for i, left in enumerate(locations[:-1]):
            for right in locations[i + 1 :]:
                x_diff = right.x - left.x
                y_diff = right.y - left.y

                for root, dir in ((left, -1), (right, 1)):
                    n = root
                    while True:
                        n = Point(n.x + dir * x_diff, n.y + dir * y_diff)
                        within_bounds = 0 <= n.x < len(data[0]) and 0 <= n.y < len(data)
                        if not within_bounds:
                            break

                        antinodes.add(n)

                        if not all_points:
                            break

    return antinodes


def test_part_1_basic():
    test_input = """..........
..........
..........
....a.....
..........
.....a....
..........
..........
..........
..........""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert _find_antinodes(data) == set([(3, 1), (6, 7)])

    assert part_1(data) == 2


def test_part_1_out_of_bounds():
    test_input = """..........
..........
..........
....a.....
........a.
.....a....
..........
..........
..........
..........""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert _find_antinodes(data) == set([(3, 1), (6, 7), (0, 2), (2, 6)])

    assert part_1(data) == 4


def atest_part_1_multiple_varietes():
    test_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_1(data) == 14


def atest_part_1_antinodes_at_antenna_locations():

    test_input = """..........
..........
..........
....a.....
........a.
.....a....
..........
......A...
..........
..........""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert _find_antinodes(data) == set([(3, 1), (6, 7), (0, 2), (2, 6)])

    assert part_1(data) == 4


def test_part_2_simple():
    test_input = """T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_2(data) == 9


def test_part_2():
    test_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_2(data) == 34
