from heapq import heappop, heappush
from typing import Generator, NamedTuple

from aoc import Solution

Heading = tuple[int, int]
Point = tuple[int, int]
State = NamedTuple(
    "State",
    [
        ("loc", Point),
        ("heading", Heading),
        ("num_steps", int),
    ],
)
Data = list

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)


def parse_input(lines: list[str]) -> Data:
    grid = []
    for row in lines:
        if not row:
            continue
        grid.append([int(c) for c in row])
    return grid


def build_moves(grid: list[str], steps_required: int = 0, step_limit: int = 3):
    max_y = len(grid)
    max_x = len(grid[0])

    def moves(state: State) -> Generator[State, None, None]:
        (x, y), current_heading, num_steps = state

        possible_moves = []

        if num_steps < step_limit:
            possible_moves.append((current_heading, num_steps + 1))

        if num_steps >= steps_required:
            # allowed to turn left and right
            dx, dy = current_heading
            possible_moves.append(((dy, -dx), 1))
            possible_moves.append(((-dy, dx), 1))

        for (dx, dy), steps in possible_moves:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < max_x and 0 <= ny < max_y:
                yield State((nx, ny), (dx, dy), steps)

    return moves


def a_star(start, h_func, moves, cost):
    queue = []
    previous = {start: None}
    costs = {start: 0}

    def add_to_queue(state):
        f = costs[state] + h_func(state)
        heappush(queue, (f, state))

    def get_path(state):
        return [] if state is None else get_path(previous[state]) + [state]

    add_to_queue(start)

    while queue:
        _, state = heappop(queue)

        if h_func(state) == 0 and state.num_steps > 3:
            return get_path(state)

        for new_state in moves(state):
            new_cost = costs[state] + cost(state, new_state)

            if new_state not in costs or new_cost < costs[new_state]:
                # same state but lower cost? Explore from here.
                costs[new_state] = new_cost
                previous[new_state] = state
                add_to_queue(new_state)

    raise Exception("Unable to find path!")


def build_h_func(data: Data, steps_required: int = 0):
    x_target = len(data[0]) - 1
    y_target = len(data) - 1

    def h_func(state: State):
        x, y = state.loc
        steps_to_destination = (x_target - x) + (y_target - y)
        missing_steps = max(steps_required - state.num_steps, 0)
        if steps_to_destination == 0 and missing_steps > 0:
            return 1_000_000_000
        return steps_to_destination

    return h_func


def build_costs(data: Data):
    def costs(_: State, s2: State):
        # minimizing heat loss, so the cost is whatever value we're moving to
        x, y = s2.loc
        cost = data[y][x]
        return cost

    return costs


def print_path(data: Data, path: list):
    headings = {NORTH: "^", SOUTH: "v", EAST: ">", WEST: "<"}
    visited = {p: headings[h] for p, h, _ in path}
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            print(visited.get((x, y), cell), end="")
        print("")


def part_1(data: Data):
    moves = build_moves(data, steps_required=0, step_limit=3)
    costs = build_costs(data)
    h_func = build_h_func(data)
    start = State((0, 0), EAST, 1)

    try:
        winning_path = a_star(start, h_func, moves, costs)
    except:
        return -1
    return sum(data[y][x] for (x, y), _, _ in winning_path[1:])


def part_2(data: Data):
    moves = build_moves(data, steps_required=4, step_limit=10)
    h_func = build_h_func(data, steps_required=4)
    costs = build_costs(data)
    start = State((0, 0), EAST, 1)

    winning_path = a_star(start, h_func, moves, costs)

    return sum(data[y][x] for (x, y), _, _ in winning_path[1:])


SOLUTION = Solution(
    day=17,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=0,
    part_2_answer=0,
)


class Test:
    DATA = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
""".split(
        "\n"
    )

    OTHER_DATA = """
111111111111
999999999991
999999999991
999999999991
999999999991
""".split(
        "\n"
    )

    def test_part_1(self):
        assert part_1(parse_input(self.DATA)) == 102

    def test_part_2(self):
        assert part_2(parse_input(self.DATA)) == 94

    def test_part_2_other(self):
        assert part_2(parse_input(self.OTHER_DATA)) == 71

    def test_part_2_ansers(self):
        assert SOLUTION.part_2() == 1149
        assert SOLUTION.part_2() < 1152


if __name__ == "__main__":
    print(SOLUTION.part_1())
    print(SOLUTION.part_2())
