from typing import Sequence

from aoc import Solution

Data = list[list[str]]


def parse_input(lines: Sequence[str]) -> Data:
    fields: Data = []
    field: list[str] = []

    for line in lines:
        if not line.strip():
            fields.append(field)
            field = []
            continue

        field.append(line)
    fields.append(field)

    return fields


def find_reflection(field: list, multiplier=100):
    for idx in range(len(field) - 1):
        matches_required = min(idx + 1, len(field) - idx - 1)
        # generator expression for lazy evaluation
        matches = (
            field[idx - offset] == field[idx + offset + 1]
            for offset in range(matches_required)
        )
        if all(matches):
            yield (idx + 1) * multiplier

    if multiplier == 100:
        rotated = ["".join(l) for l in zip(*field)]
        yield from find_reflection(rotated, multiplier=1)


def fix_smudge(field: list):
    old_reflection_lines = next(find_reflection(field))

    for y, row in enumerate(field):
        for x, char in enumerate(row):
            new_char = "." if char == "#" else "#"
            new_row = "".join([row[:x], new_char, row[x + 1 :]])
            new_field = field[:y] + [new_row] + field[y + 1 :]

            reflection_line = find_reflection(new_field)
            for l in reflection_line:
                if l != old_reflection_lines:
                    return l
    return 0


def part_1(data: Data):
    return sum(next(find_reflection(field)) for field in data)


def part_2(data: Data):
    return sum(fix_smudge(field) for field in data)


SOLUTION = Solution(
    day=13,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=43614,
    part_2_answer=36771,
)


class Tests:
    DATA = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".split(
        "\n"
    )

    def test_parsing(self):
        data = parse_input(self.DATA)

    def test_part_1(self):
        data = parse_input(self.DATA)
        assert part_1(data) == 405

    def test_part_1_single(self):
        data = parse_input(
            """
...#..##.####.#
##..##.###..###
#.#............
#...#...#..#.#.
.#..###.#.##.#.
###.###.##..##.
.....##........
##..#....#..#..
#....#...#..#..
#..##.#.#.##.#.
#..##.#.#.##.#.
#....#...#..#..
##..#....#..#..
.....##........
###.###.##..##.""".split(
                "\n"
            )
        )
        assert part_1(data[1:]) == 1000

    def test_part_1_single2(self):
        data = parse_input(
            """
#...#..#.
#...#..#.
.####..#.
..#..#..#
...#....#
##..###..
#...####.
#...####.
##..##...
...#....#
..#..#..#
.####..#.
#...#..#.""".split(
                "\n"
            )
        )
        assert part_1(data[1:]) == 100

    def test_part_1_size(self):
        assert SOLUTION.part_1() > 38623
        assert SOLUTION.part_1() > 43210

    def test_part_2(self):
        data = parse_input(self.DATA)
        assert part_2(data) == 400

    def test_part_2_size(self):
        assert SOLUTION.part_2() > 34038
        assert SOLUTION.part_2() < 43838
        assert SOLUTION.part_2() > 34117


if __name__ == "__main__":
    print(SOLUTION.part_1(), SOLUTION.part_1_solved)
    print(SOLUTION.part_2(), SOLUTION.part_2_solved)
