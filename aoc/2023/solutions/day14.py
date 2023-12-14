from typing import Callable, Iterable, Sequence

from solution import Solutions

Point = tuple[int, int]
Data = tuple[set[Point], set[Point]]


def parse_input(lines: Sequence[str]) -> Data:
    movable: set[Point] = set()
    immovable: set[Point] = set()
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            if char == "O":
                movable.add((x, y))
            if char == "#":
                immovable.add((x, y))
    return movable, immovable


def tilt(
    immovable: set[Point],
    rocks: Iterable[Point],
    new_positions: Callable[[Point], Iterable[Point]],
):
    new_locations: set[Point] = set()
    for rock in rocks:
        new_pos_stack = []
        for new_pos in new_positions(rock):
            if new_pos in immovable or new_pos in new_locations:
                # hit a rock, can't go further
                break
            new_pos_stack.append(new_pos)

        # either last place we landed, or we haven't moved at all
        settled_pos = new_pos_stack.pop() if new_pos_stack else rock
        new_locations.add(settled_pos)
    return new_locations


from itertools import cycle


def tilt_north(moveable: set[Point], immovable: set[Point]) -> set[Point]:
    return tilt(
        immovable=immovable,
        rocks=sorted(moveable, key=lambda p: p[1]),
        new_positions=lambda rock: zip(cycle([rock[0]]), range(rock[1], -1, -1)),
    )


def tilt_south(moveable: set[Point], immovable: set[Point]) -> set[Point]:
    max_y = max(p[1] for p in immovable)
    return tilt(
        immovable=immovable,
        rocks=sorted(moveable, key=lambda p: p[1], reverse=True),
        new_positions=lambda rock: zip(cycle([rock[0]]), range(rock[1], max_y + 1)),
    )


def tilt_east(moveable: set[Point], immovable: set[Point]) -> set[Point]:
    max_x = max(p[0] for p in immovable)
    return tilt(
        immovable=immovable,
        rocks=sorted(moveable, key=lambda p: p[0], reverse=True),
        new_positions=lambda rock: zip(range(rock[0], max_x + 1), cycle([rock[1]])),
    )


def tilt_west(moveable: set[Point], immovable: set[Point]) -> set[Point]:
    return tilt(
        immovable=immovable,
        rocks=sorted(moveable, key=lambda p: p[0]),
        new_positions=lambda rock: zip(range(rock[0], -1, -1), cycle([rock[1]])),
    )


def do_cycle(moveable: set[Point], immovable: set[Point]) -> set[Point]:
    for f in [tilt_north, tilt_west, tilt_south, tilt_east]:
        moveable = f(moveable, immovable)
    return moveable


def print_rocks(moveable: set, immovable: set):
    max_x = max(p[0] for p in immovable)
    max_y = max(p[1] for p in immovable)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in moveable:
                print("O", end="")
            elif (x, y) in immovable:
                print("#", end="")
            else:
                print(".", end="")

        print("")


def part_1(data: Data):
    moveable, immovable = data
    max_y = max(p[1] for p in immovable)
    moveable = tilt_north(moveable, immovable)

    total = 0
    for rock in moveable:
        total += max_y - rock[1] + 1

    return total


def part_2(data: Data):
    moveable, immovable = data

    seen = []

    n = 0
    while True:
        if moveable in seen:
            cycle_length = n - seen.index(moveable)
            break
        seen.append(moveable)

        moveable = do_cycle(moveable, immovable)
        n += 1

    cycle_start = n - cycle_length
    target = (1_000_000_000 - cycle_start) % cycle_length
    remaining_steps = target % n
    for n in range(remaining_steps):
        moveable = do_cycle(moveable, immovable)

    max_y = max(p[1] for p in immovable)
    total = 0
    for rock in moveable:
        total += max_y - rock[1] + 1

    return total


SOLUTION = Solutions(
    day=14,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=109665,
    part_2_answer=96061,
)


class Tests:
    DATA = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".split(
        "\n"
    )

    def test_parsing(self):
        movable = {
            (0, 1),
            (7, 4),
            (5, 5),
            (2, 1),
            (9, 3),
            (0, 0),
            (3, 1),
            (4, 3),
            (9, 6),
            (0, 3),
            (7, 7),
            (1, 4),
            (2, 9),
            (2, 6),
            (0, 5),
            (6, 6),
            (1, 3),
            (1, 9),
        }
        immovable = {
            (6, 2),
            (8, 4),
            (5, 8),
            (6, 8),
            (0, 9),
            (9, 5),
            (3, 3),
            (5, 0),
            (2, 5),
            (5, 6),
            (7, 8),
            (5, 9),
            (7, 5),
            (9, 1),
            (4, 1),
            (0, 8),
            (5, 2),
        }
        assert parse_input(self.DATA) == (movable, immovable)

    def test_tilt(self):
        moveable, immovable = parse_input(self.DATA)
        new_locations = tilt_north(moveable, immovable)

        print_rocks(new_locations, immovable)

        assert (
            parse_input(
                """OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
""".split(
                    "\n"
                )
            )[0]
            == new_locations
        )

    def test_part_1(self):
        assert part_1(parse_input(self.DATA)) == 136

    def test_cycle(self):
        moveable, immovable = parse_input(self.DATA)
        moveable = do_cycle(moveable, immovable)

        print_rocks(moveable, immovable)
        assert (
            parse_input(
                """.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....""".split(
                    "\n"
                )
            )[0]
            == moveable
        )

    def test_part_2(self):
        assert part_2(parse_input(self.DATA)) == 64


if __name__ == "__main__":
    print(SOLUTION.part_1(), SOLUTION.part_1_solved)
    print(SOLUTION.part_2(), SOLUTION.part_2_solved)
