from typing import Callable

from aoc import Solution

Point = tuple[int, int]
Heading = complex
Data = list[str]


def parse_input(lines: list[str]) -> Data:
    return lines[:-1]


def change_heading(cell: str, heading: complex) -> list[complex]:
    if cell == ".":
        return [heading]

    if cell == "-":
        if heading.real:
            return [heading]
        return [1, -1]

    if cell == "|":
        if heading.imag:
            return [heading]
        return [1j, -1j]

    if cell == "/":
        if heading.real:
            return [heading * -1j]
        return [heading * 1j]

    if cell == "\\":
        if heading.real:
            return [heading * 1j]
        return [heading * -1j]
    raise ValueError(f"Not supposed to get here! Heading: {heading}")


def build_beam_advancer(grid: Data):
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1

    def advance_beam(loc: Point, heading: complex):
        x, y = loc
        for new_heading in change_heading(grid[y][x], heading):
            nx, ny = x + int(new_heading.real), y + int(new_heading.imag)
            within_bounds = 0 <= nx <= max_x and 0 <= ny <= max_y
            if not within_bounds:
                continue

            yield (nx, ny), new_heading

    return advance_beam


def num_energized(start: Point, heading: complex, beam_advancer: Callable):
    visited = set()
    headings: list[tuple[Point, Heading]] = [(start, heading)]
    while headings:
        new_headings = []

        for loc, heading in headings:
            if (loc, heading) in visited:
                # been here in this direction before, can skip
                continue
            visited.add((loc, heading))
            new_headings.extend(beam_advancer(loc, heading))

        headings = new_headings
    return len(set(p for p, _ in visited))


def part_1(data: Data):
    beam_advancer = build_beam_advancer(data)
    return num_energized((0, 0), 1, beam_advancer)


def part_2(data: Data):
    beam_advancer = build_beam_advancer(data)
    max_x = len(data[0]) - 1
    max_y = len(data) - 1

    def gen_headings():
        for y in range(len(data)):
            # left side
            yield ((0, y), 1)
            # right side
            yield ((max_x, y), -1)
        for x in range(len(data[0])):
            # top side
            yield ((x, 0), 1j)
            # bottom side
            yield ((x, max_y), -1j)

    return max(
        num_energized(start, heading, beam_advancer)
        for start, heading in gen_headings()
    )


SOLUTION = Solution(
    day=16,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=7472,
    part_2_answer=7716,
)


class Tests:
    DATA = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""".split(
        "\n"
    )

    def test_part_1(self):
        assert part_1(parse_input(self.DATA)) == 46

    def test_part_2(self):
        assert part_2(parse_input(self.DATA)) == 51

    def test_change_heading(self):
        assert change_heading(".", 1) == [1]

        assert change_heading("-", 1) == [1]
        assert change_heading("-", -1) == [-1]
        assert change_heading("-", 1j) == [1, -1]
        assert change_heading("-", 1j) == [1, -1]

        assert change_heading("|", 1j) == [1j]
        assert change_heading("|", -1j) == [-1j]
        assert change_heading("|", 1) == [1j, -1j]
        assert change_heading("|", -1) == [1j, -1j]

        assert change_heading("/", 1) == [-1j]
        assert change_heading("/", 1j) == [-1]
        assert change_heading("/", -1) == [1j]
        assert change_heading("/", -1j) == [1]

        assert change_heading("\\", 1) == [1j]
        assert change_heading("\\", 1j) == [1]
        assert change_heading("\\", -1) == [-1j]
        assert change_heading("\\", -1j) == [-1]

    def test_sol_part_1(self):
        assert SOLUTION.part_1() > 266


if __name__ == "__main__":
    print(SOLUTION.part_1())
    print(SOLUTION.part_2())
