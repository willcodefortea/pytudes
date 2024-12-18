import re
import heapq
from typing import Callable, NamedTuple, Sequence, TypeVar

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
    if not winning_path:
        return -1
    return len(winning_path) - 1


def part_2(all_bytes: Data, size: tuple[int, int] = (70, 70)):
    neighbours = bounded_neighbours(limits=(size[0] + 1, size[1] + 1))

    def h_func(loc: Point):
        return (size[0] - loc.x) + (size[1] - loc.y)

    indexed_bytes = list(zip(range(len(all_bytes)), all_bytes))

    def take_right(indexed_byte: tuple[int, Point]):
        index, _ = indexed_byte

        def moves(loc: Point):
            return tuple(
                neighbour
                for neighbour in neighbours(loc)
                if neighbour not in all_bytes[:index]
            )

        maybe_path = a_star(Point(0, 0), moves, h_func)
        return maybe_path is not None

    pivot_points = list(
        binary_walk(indexed_bytes, 0, len(all_bytes) - 1, take_right=take_right)
    )
    last_good_byte = next(
        byte for (_, byte), valid_path in pivot_points[::-1] if valid_path
    )
    return f"{last_good_byte.x},{last_good_byte.y}"


T = TypeVar("T")


def binary_walk(items: list[T], low: int, high: int, take_right: Callable[[T], bool]):
    if low > high:
        return

    pivot = (high + low) // 2

    should_go_right = take_right(items[pivot])
    yield items[pivot], should_go_right

    if should_go_right:
        yield from binary_walk(items, pivot + 1, high, take_right)
    else:
        yield from binary_walk(items, low, pivot - 1, take_right)


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
