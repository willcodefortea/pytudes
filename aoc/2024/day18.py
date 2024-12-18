import re
import heapq
from typing import Callable, NamedTuple, Sequence

import aoc

Point = NamedTuple("Point", (("x", int), ("y", int)))
Data = list[Point]


def parse_input(lines: Sequence[str]) -> Data:
    data: Data = []
    for line in lines:
        if not line:
            continue
        x, y = map(int, re.findall(r"\d+", line))
        data.append(Point(x, y))

    return data


def part_1(data: Data, size: tuple[int, int] = (70, 70)):
    neighbours = bounded_neighbours(limits=(size[0] + 1, size[1] + 1))

    data = data[:1024]

    def moves(loc: Point):
        return tuple(
            neighbour for neighbour in neighbours(loc) if neighbour not in data
        )

    def h_func(loc: Point):
        return (size[0] - loc.x) + (size[1] - loc.y)

    start = Point(0, 0)
    winning_path = a_star(start, moves, h_func)
    return len(winning_path) - 1 if winning_path else -1


def part_2(all_bytes: Data, size: tuple[int, int] = (70, 70)):
    cutoff = 0

    neighbours = bounded_neighbours(limits=(size[0] + 1, size[1] + 1))

    def h_func(loc: Point):
        return (size[0] - loc.x) + (size[1] - loc.y)

    last_winning_path: list[Point] = []
    for cutoff in range(len(all_bytes)):
        data = all_bytes[:cutoff]
        new_byte = all_bytes[cutoff - 1]

        if last_winning_path and new_byte not in last_winning_path:
            # no point evaluating, our previous path still wins!
            continue

        def moves(loc: Point):
            return tuple(
                neighbour for neighbour in neighbours(loc) if neighbour not in data
            )

        start = Point(0, 0)
        maybe_path = a_star(start, moves, h_func)

        if maybe_path is None:
            # no path to exit, previous point is the winner
            x, y = all_bytes[cutoff - 1]
            return f"{x},{y}"

        last_winning_path = maybe_path


def a_star(
    start: Point,
    moves: Callable[[Point], Sequence[Point]],
    h_func: Callable[[Point], int],
    cost=lambda s1, s2: 1,
) -> list[Point] | None:
    queue = []
    costs = {start: 0}
    previous = {start: None}

    def add_to_queue(state: Point):
        heapq.heappush(queue, (costs[state] + h_func(state), state))

    def get_path(state: Point | None):
        if not state:
            return []
        return get_path(previous[state]) + [state]

    add_to_queue(start)

    while queue:
        _, state = heapq.heappop(queue)

        if h_func(state) == 0:
            return get_path(state)

        for new_state in moves(state):
            new_cost = costs[state] + cost(state, new_state)

            if new_state not in costs or new_cost < costs[new_state]:
                costs[new_state] = new_cost
                previous[new_state] = state
                add_to_queue(new_state)

    return None


def neighbours(loc: Point):
    deltas = ((1, 0), (0, 1), (-1, 0), (0, -1))
    return (Point(x=loc.x + dx, y=loc.y + dy) for dx, dy in deltas)


def bounded_neighbours(limits: tuple[int, int]):
    max_x, max_y = limits

    def bounded(loc: Point):
        return (
            neighbour
            for neighbour in neighbours(loc)
            if 0 <= neighbour.x < max_x and 0 <= neighbour.y < max_y
        )

    return bounded


SOLUTION = aoc.Solution(
    day=18,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=272,
    part_2_answer="16,44",
)


def test_part_1():
    test_input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_1(data[:12], (6, 6)) == 22


def test_part_2():
    test_input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""".split(
        "\n"
    )
    data = parse_input(test_input)
    assert part_2(data, (6, 6)) == "6,1"
