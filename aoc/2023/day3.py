from collections import defaultdict
from re import L

test_data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

data = open("day3.txt").read()


def get_neighbours(x: int, y: int, grid: list[str]):
    neighbours_8 = (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)

    neighbours: list[tuple[int, int, str]] = []
    for dx, dy in neighbours_8:
        try:
            neighbours.append(
                (
                    x + dx,
                    y + dy,
                    grid[y + dy][x + dx],
                )
            )
        except IndexError:
            continue

    return neighbours


def build_engine_graph(engine: list[str]):
    graphs = []

    numbers = "0123456789"

    for y, line in enumerate(engine):
        part = ""
        symbols = set()

        for x, char in enumerate(line):
            if char not in numbers:
                if part:
                    graphs.append((int(part), symbols))

                # reset
                symbols = set()
                part = ""
                continue

            part += char
            for nx, ny, neighbour in get_neighbours(x, y, engine):
                is_symbol = neighbour not in "." + numbers
                if is_symbol:
                    symbols.add((nx, ny, neighbour))

        if part:
            # reset
            graphs.append((int(part), symbols))
            part = ""
            symbols = set()

    return graphs


def extract_engine_parts(engine: list[str]) -> list[int]:
    graphs = build_engine_graph(engine)
    return [part for part, symbols in graphs if len(symbols) > 0]


print(extract_engine_parts(test_data.split("\n")))
test_part_1 = sum(extract_engine_parts(test_data.split("\n")))
print(test_part_1)
assert test_part_1 == 4361


part_1 = sum(extract_engine_parts(data.split("\n")))
print(f"Part 1: {part_1}")
assert part_1 > 519861, part_1


def gear_ratio(engine: list[str]):
    graphs = build_engine_graph(engine)

    gear_graph = defaultdict(list)

    for part, symbols in graphs:
        for nx, ny, symbol in symbols:
            if symbol != "*":
                continue

            gear_graph[(nx, ny)].append(part)

    total = 0
    for parts in gear_graph.values():
        if len(parts) != 2:
            continue

        total += parts[0] * parts[1]
    return total


print(gear_ratio(data.split("\n")))
