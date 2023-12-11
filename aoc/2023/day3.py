from collections import defaultdict

from solution import Solutions


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


Graph = tuple[int, set[str]]


def build_engine_graph(engine: list[str]):
    graphs: list[Graph] = []

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


def extract_engine_parts(graphs: list[Graph]) -> list[int]:
    return [part for part, symbols in graphs if len(symbols) > 0]


def part_1(graphs: list[Graph]):
    return sum(extract_engine_parts(graphs))


def part_2(graphs: list[Graph]):
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


SOLUTION = Solutions(
    day=3,
    part_1=part_1,
    part_2=part_2,
    parse_data=build_engine_graph,
    part_1_answer=520019,
    part_2_answer=75519888,
)

if __name__ == "__main__":
    print(SOLUTION.part_1(), SOLUTION.part_1_solved)
    print(SOLUTION.part_2(), SOLUTION.part_2_solved)
