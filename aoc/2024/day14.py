"""
Day 14: Restroom Redoubt

Phew the second part I thought I'd need to manually detech when robots are close
to one another, then print if it was > 50%. Thankfully I just checked if there
were no overlaps, and that was the answer. \o/

1111111111111111111111111111111
1.............................1
1.............................1
1.............................1
1.............................1
1..............1..............1
1.............111.............1
1............11111............1
1...........1111111...........1
1..........111111111..........1
1............11111............1
1...........1111111...........1
1..........111111111..........1
1.........11111111111.........1
1........1111111111111........1
1..........111111111..........1
1.........11111111111.........1
1........1111111111111........1
1.......111111111111111.......1
1......11111111111111111......1
1........1111111111111........1
1.......111111111111111.......1
1......11111111111111111......1
1.....1111111111111111111.....1
1....111111111111111111111....1
1.............111.............1
1.............111.............1
1.............111.............1
1.............................1
1.............................1
1.............................1
1.............................1
1111111111111111111111111111111
"""

from collections import defaultdict
from functools import reduce
import re
from typing import NamedTuple, Sequence

import aoc

Point = NamedTuple("Point", (("x", int), ("y", int)))
Robot = NamedTuple("Robot", (("position", Point), ("velocity", Point)))
Data = list[Robot]


def parse_input(lines: Sequence[str]) -> Data:
    data: Data = []
    for line in lines:
        if not line:
            break

        matches = re.findall(r"-?\d+", line)
        px, py, vx, vy = [int(num) for num in matches]
        robot = Robot(position=Point(x=px, y=py), velocity=Point(x=vx, y=vy))
        data.append(robot)
    return data


def part_1(data: Data, size=Point(101, 103)):
    for _ in range(100):
        data = list(_advance(data, size))

    return _sum_quadrants(
        robots=data,
        size=size,
    )


def _sum_quadrants(robots: Data, size: Point):
    counts = defaultdict(int)
    half_x = size.x // 2
    half_y = size.y // 2

    in_quadrants = (
        robot
        for robot in robots
        if robot.position.x != half_x and robot.position.y != half_y
    )
    for robot in in_quadrants:
        x_half = robot.position.x < size.x // 2
        y_half = robot.position.y < size.y // 2
        counts[(x_half, y_half)] += 1

    return reduce(lambda a, b: a * b, counts.values(), 1)


def _advance(robots: Sequence[Robot], size: Point):
    for robot in robots:
        yield Robot(
            position=Point(
                x=(robot.position.x + robot.velocity.x) % size.x,
                y=(robot.position.y + robot.velocity.y) % size.y,
            ),
            velocity=robot.velocity,
        )


def _print_robots(robots: Data, size: Point):
    robot_positions = defaultdict(int)

    for robot in robots:
        robot_positions[robot.position] += 1

    for y in range(size.y):
        for x in range(size.x):
            print(robot_positions.get((x, y), "."), end="")
        print("")


def part_2(data: Data, size=Point(101, 103)):
    for step in range(1, 10000):
        data = list(_advance(data, size))

        # assume no overlaps??
        if len(set((r.position) for r in data)) == len(data):
            # uncomment to see the output
            # _print_robots(data, size)
            return step


SOLUTION = aoc.Solution(
    day=14,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=221142636,
    part_2_answer=7916,
)


def test_part_1():
    test_input = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_1(data, size=Point(11, 7)) == 12
