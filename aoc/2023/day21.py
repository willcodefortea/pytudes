from aoc import Solution

Data = tuple[dict, tuple[int, int]]


def parse_input(lines: list[str]) -> Data:
    lines = lines[:-1]
    graph = {}

    deltas = (0, 1), (0, -1), (1, 0), (-1, 0)

    y_max = len(lines)
    x_max = len(lines[0])
    start = (0, 0)

    for y, row in enumerate(lines):
        for x, cell in enumerate(row):
            is_rock = cell == "#"
            if is_rock:
                continue

            is_start = cell == "S"
            if is_start:
                start = (x, y)

            graph[(x, y)] = set(
                (x + dx, y + dy)
                for dx, dy in deltas
                if 0 <= x + dx < x_max
                and 0 <= y + dy < y_max
                and lines[y + dy][x + dx] in ".S"
            )
    return graph, start


def part_1(data: Data, num_steps: int = 64):
    graph, start = data

    locations = set([start])
    for _ in range(num_steps):
        next_locations = set()

        for loc in locations:
            next_locations.update(graph[loc])

        locations = next_locations
    return len(locations)


def part_2(data: Data):
    return 0


SOLUTION = Solution(
    day=21,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=3585,
    part_2_answer=-1,
)


class Test:
    DATA = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
""".split(
        "\n"
    )

    def test_part_1(self):
        assert part_1(parse_input(self.DATA), 6) == 16


if __name__ == "__main__":
    print(SOLUTION.part_1())
    print(SOLUTION.part_2())
