"""
Day 12: Garden Groups

So today's nearly broke me. You can tell from the number of tests that I
struggled with this one!

The key insight for me on part 2 was that the number of edges is equal to the
number of corners, so all we have to do is find the corners, how hard can that
be?

Turns out, fiddly.

Some properties about corners:

    * they can happen in any diagonal from point
    * they can face out or in
    * if they face out, then the two adjacent points must be occupied
    * if they face in, then the two adjacent points must be empty


Here's a diagaram that might help (I drew a bunch in excalidraw..)

  .....        .....
  .X...        .X...
  .XX..   ->   AXX..
  .....        CA...

  ^ here X is the plot, C is the corner being inspected, and A are the adjacent
  points

With these properties we can cobble together an algorthim to count them
properly.

The examples were incredibly useful for testing and debugging.
"""

from collections import defaultdict
from typing import Any, NamedTuple, Sequence

import aoc

Data = list[str]
Point = NamedTuple("Point", (("x", int), ("y", int)))


def parse_input(lines: Sequence[str]) -> Data:
    return [l for l in lines if l]


def part_1(data: Data):
    # TODO: clean up?
    visited = set()

    total = 0
    for y in range(len(data)):
        for x in range(len(data[0])):
            if (x, y) in visited:
                continue

            # haven't explored here before
            char = data[y][x]
            to_visit = [Point(x, y)]
            area = 0
            perimiter = 0

            while to_visit:
                visiting = to_visit.pop()
                if visiting in visited:
                    continue
                visited.add(visiting)
                area += 1
                perimiter += 4
                for np in _neighbours(data, visiting):
                    nx, ny = np
                    if data[ny][nx] == char:
                        if np not in visited:
                            to_visit.append(np)
                        perimiter -= 1

            total += area * perimiter
    return total


def part_2(data: Data):
    plots = _find_plots(data)

    total = 0
    for plot in plots.values():
        corners = _count_couners(plot)
        area = len(plot)
        total += corners * area

    return total


def _count_couners(plot: list[Point]):
    num_corners = 0

    corner_deltas = (
        (-1, -1),  # top left
        (1, -1),  # top right
        (1, 1),  # bottom right
        (-1, 1),  # bottom left
    )

    for px, py in plot:
        for dx, dy in corner_deltas:
            cx, cy = px + dx, py + dy
            corner = Point(cx, cy)

            h_neighbour = Point(cx, py)
            v_neighbour = Point(px, cy)
            num_occupied = int(h_neighbour in plot) + int(v_neighbour in plot)

            is_internal = corner in plot and num_occupied > 0
            if is_internal:
                continue

            outer_corner = num_occupied == 0
            inner_corner = num_occupied == 2
            if outer_corner or inner_corner:
                num_corners += 1

    return num_corners


def _find_plots(grid: Sequence[str]):
    plots: dict[tuple[int, str], list[Point]] = defaultdict(list)
    visited = set()

    plot_num = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) in visited:
                continue

            plot_num += 1
            plot_char = grid[y][x]

            to_visit = [Point(x, y)]
            while to_visit:
                visiting = to_visit.pop()
                if visiting in visited:
                    continue
                visited.add(visiting)
                plots[plot_num, plot_char].append(visiting)

                for np in _neighbours(grid, visiting):
                    nx, ny = np
                    if grid[ny][nx] != plot_char:
                        continue

                    if np not in visited:
                        to_visit.append(np)
    return plots


def _neighbours(grid: Sequence[Sequence[Any]], point: Point):
    deltas = ((1, 0), (0, 1), (-1, 0), (0, -1))

    for dx, dy in deltas:
        nx, ny = point.x + dx, point.y + dy

        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            yield Point(x=nx, y=ny)


SOLUTION = aoc.Solution(
    day=12,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=1464678,
    part_2_answer=877492,
)


def test_part_1_simple():
    test_input = """AAAA
BBCD
BBCC
EEEC""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_1(data) == 140


def test_part_1_larger():
    test_input = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_1(data) == 1930


def test_part_2_no_neighbours():
    test_input = """X""".split("\n")
    data = parse_input(test_input)
    assert part_2(data) == 4


def test_part_2_pipe():
    test_input = """XXX""".split("\n")
    data = parse_input(test_input)
    assert part_2(data) == 12


def test_part_2_vertical_pipe():
    test_input = """X
X
X""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_2(data) == 12


def test_part_2_square():
    test_input = """XX
XX""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_2(data) == 16


def test_part_2_l_shape():
    test_input = """Xa
XX""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_2(data) == 18 + 4


def test_part_2_small():
    test_input = """AAAA
BBCD
BBCC
EEEC""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_2(data) == 80


def test_part_2_e_shape():
    test_input = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_2(data) == 236


def test_part_2_complex():
    test_input = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_2(data) == 368


def test_part_2_big():
    test_input = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_2(data) == 1206
