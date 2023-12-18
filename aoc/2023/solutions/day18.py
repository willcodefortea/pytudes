import re

from solution import Solutions

Data = list[tuple[str, int]]


DIRECTIONS = {"U": -1j, "D": 1j, "L": -1, "R": 1}


def parse_input(lines: list[str]) -> Data:
    data = []
    for line in lines:
        if not line:
            continue
        direction, amount = re.match(r"(\w) (\d+)", line).groups()
        data.append((direction, int(amount)))
    return data


def part_1(data: Data):
    visited = set([0])

    current = 0
    for direction, amount in data:
        delta = DIRECTIONS[direction]

        for _ in range(amount):
            current += delta
            visited.add(current)

    # loop from left to right, and count number of cells inside
    min_x = min(int(n.real) for n in visited)
    max_x = max(int(n.real) for n in visited)
    min_y = min(int(n.imag) for n in visited)
    max_y = max(int(n.imag) for n in visited)

    inside_count = 0
    for y in range(min_y, max_y + 1):
        inside = False
        for x in range(min_x, max_x + 1):
            node = x + y * 1j
            north_node = x + (y - 1) * 1j

            if node in visited and north_node in visited:
                inside = not inside
                continue

            inside_count += inside and node not in visited

    return inside_count + len(visited)


def part_2(data: Data):
    return 0


SOLUTION = Solutions(
    day=18,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=76387,
    part_2_answer=-1,
)


class Tests:
    DATA = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""".split(
        "\n"
    )

    def test_part_1(self):
        assert part_1(parse_input(self.DATA)) == 62


if __name__ == "__main__":
    print(SOLUTION.part_1())
    print(SOLUTION.part_2())
