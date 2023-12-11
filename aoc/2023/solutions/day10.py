from solution import Solutions

test_data_loop = """.....
.S-7.
.|.|.
.L-J.
.....""".split(
    "\n"
)

test_data = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

Point = tuple[int, int]

NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)
DELTAS: dict[str, tuple] = {
    "|": (NORTH, SOUTH),
    "-": (EAST, WEST),
    "L": (NORTH, EAST),
    "J": (NORTH, WEST),
    "7": (SOUTH, WEST),
    "F": (SOUTH, EAST),
    ".": tuple(),
}


def parse_input(lines: list[str]):
    graph: dict[Point, list[Point]] = {}

    start = (0, 0)
    start_char = "|"

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            p = (x, y)

            if char == "S":
                start = p
                continue

            connected_nodes = [(x + dx, y + dy) for dx, dy in DELTAS[char]]
            if connected_nodes:
                graph[p] = connected_nodes

    # now find a piece that fits as a loop in the starting location
    x, y = start
    for char, deltas in DELTAS.items():
        nodes = [(x + dx, y + dy) for (dx, dy) in deltas]
        if not nodes:
            continue

        for node in nodes:
            if start not in graph.get(node, []):
                break
        else:
            # clean exit, all pipes connected
            graph[start] = nodes
            start_char = char

    return start, start_char, graph, lines


def part_1(data):
    start, _, graph, _ = data

    current_node = start
    nodes_visited = set()

    while current_node not in nodes_visited:
        nodes_visited.add(current_node)

        for node in graph[current_node]:
            if node not in nodes_visited:
                current_node = node
    return len(nodes_visited) // 2


def find_main_loop(start: Point, graph: dict[Point, list[Point]]):
    main_loop = set([start])
    to_explore = [start]

    while to_explore:
        current = to_explore.pop()
        for node in graph[current]:
            if node in main_loop:
                continue
            main_loop.add(node)
            to_explore.append(node)
    return main_loop


def part_2(data):
    start, start_char, graph, lines = data
    # we're doing a "point in a polygon" solution.
    # drawing left to right across the grid we can tell if we're inside if we
    # cross a line that is travelling north.
    main_loop = find_main_loop(start, graph)

    # clone the lines are we're mutating one
    lines = lines[:]
    _, start_y = start
    lines[start_y] = lines[start_y].replace("S", start_char)

    north_chars = [k for k, v in DELTAS.items() if NORTH in v]
    total_inside = 0
    for y, line in enumerate(lines):
        # start on the outside...
        is_inside = False
        for x, char in enumerate(line):
            p = (x, y)

            if char in north_chars and p in main_loop:
                # ...cross a northern line in the main loop, so flip is_inside
                is_inside = not is_inside

            total_inside += int(is_inside and p not in main_loop)
    return total_inside


class Tests:
    def test_start_coordinates(self):
        assert parse_input(test_data_loop)[0] == (1, 1)

    def test_graph_construction_circle(self):
        assert parse_input(test_data_loop)[2] == {
            (2, 1): [(3, 1), (1, 1)],
            (3, 1): [(3, 2), (2, 1)],
            (1, 2): [(1, 1), (1, 3)],
            (3, 2): [(3, 1), (3, 3)],
            (1, 3): [(1, 2), (2, 3)],
            (2, 3): [(3, 3), (1, 3)],
            (3, 3): [(3, 2), (2, 3)],
            (1, 1): [(1, 2), (2, 1)],
        }

    def test_part1_loop(self):
        assert part1(test_data_loop) == 4

    def test_loop_enclosure(self):
        loop = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""".split(
            "\n"
        )
        assert part2(parse_input(loop)) == 4

    def test_loop_enclosure_no_gap(self):
        loop = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........""".split(
            "\n"
        )
        assert part2(parse_input(loop)) == 4

    def test_larger(self):
        loop = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""".split(
            "\n"
        )

        assert part2(parse_input(loop)) == 8

    def test_larger_with_junk(self):
        loop = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""".split(
            "\n"
        )
        assert part2(parse_input(loop)) == 10


SOLUTION = Solutions(
    day=10,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=6697,
    part_2_answer=423,
)

if __name__ == "__main__":
    print(SOLUTION.part_1(), SOLUTION.part_1_solved)
    print(SOLUTION.part_2(), SOLUTION.part_2_solved)
