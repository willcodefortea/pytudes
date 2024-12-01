from functools import partial

from aoc import Solution

test_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".split(
    "\n"
)

test_input_grown = """....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......""".split(
    "\n"
)


def parse_input(lines: list[str]):
    non_empty_cols: set[int] = set()
    non_empty_rows: set[int] = set()

    galaxies: list[tuple[int, int]] = []

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.append((x, y))
                non_empty_cols.add(y)
                non_empty_rows.add(x)

    return galaxies


def grow_space(galaxies: list[tuple[int, int]], factor: int = 2):
    all_x, all_y = zip(*galaxies)

    empty_x = set(range(max(all_x))) - set(all_x)
    empty_y = set(range(max(all_y))) - set(all_y)

    # every empty row / column is replaced with `factor` others,
    # but because we add on to other locations one row / column
    # is already accounted for, so remove it here
    factor -= 1

    moved_galaxies = galaxies[:]

    # grow cols
    for x in sorted(empty_x):
        for idx, (gx, _) in enumerate(galaxies):
            dx = 0 if gx < x else factor
            mx, my = moved_galaxies[idx]
            moved_galaxies[idx] = (mx + dx, my)

    # grow rows
    for y in sorted(empty_y):
        for idx, (_, gy) in enumerate(galaxies):
            dy = 0 if gy < y else factor
            mx, my = moved_galaxies[idx]
            moved_galaxies[idx] = (mx, my + dy)

    return moved_galaxies


def pairwise(some_list: list):
    for idx, a in enumerate(some_list[:-1]):
        for b in some_list[idx + 1 :]:
            yield a, b


def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def part_1(galaxies):
    galaxies = grow_space(galaxies)
    return sum(manhattan_distance(*pair) for pair in pairwise(galaxies))


def part_2(galaxies, growth_factor: int):
    galaxies = grow_space(galaxies, growth_factor)
    return sum(manhattan_distance(*pair) for pair in pairwise(galaxies))


class Tests:
    def test_growth(self):
        assert parse_input(test_input_grown) == grow_space(parse_input(test_input))

    def test_part_1(self):
        assert part_1(parse_input(test_input)) == 374

    def test_part_2(self):
        assert part_2(parse_input(test_input), 10) == 1030
        assert part_2(parse_input(test_input), 100) == 8410


SOLUTION = Solution(
    day=11,
    part_1=part_1,
    part_2=partial(part_2, growth_factor=1_000_000),
    parse_data=parse_input,
    part_1_answer=9599070,
    part_2_answer=842645913794,
)

if __name__ == "__main__":
    print(SOLUTION.part_1(), SOLUTION.part_1_solved)
    print(SOLUTION.part_2(), SOLUTION.part_2_solved)
