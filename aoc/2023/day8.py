import math
import re
from itertools import cycle

from solution import Solutions

test_input = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""".split(
    "\n"
)

Nodes = dict[str, tuple[str, str]]


def parse_input(lines: list[str]) -> tuple[str, Nodes]:
    instructions = lines[0].strip()
    nodes = {}

    for line in lines[2:]:
        if not line:
            continue

        name, left, right = re.match(r"(\w+) = \((\w+), (\w+)\)", line).groups()
        nodes[name] = (left, right)
    return instructions, nodes


def follow_instructions(instructions: str, nodes: Nodes, start: str):
    node = start
    for instruction_num, instruction in enumerate(cycle(instructions)):
        idx = 0 if instruction == "L" else 1
        node = nodes[node][idx]

        instruction_idx = instruction_num % len(instructions)

        yield instruction_idx, node


def part_1(data):
    instructions, nodes = data
    num_steps = 0
    for _, node in follow_instructions(instructions, nodes, "AAA"):
        num_steps += 1
        if node == "ZZZ":
            break
    return num_steps


def part_2(data) -> int:
    instructions, nodes = data

    starting_locations = [n for n in nodes if n.endswith("A")]
    cycles: list[int] = []
    for node in starting_locations:
        # store the instruction index and current node value
        seen = set()
        num_steps = 0
        first_visit: dict[str, int] = {}

        for loc in follow_instructions(instructions, nodes, node):
            _, node = loc

            if node not in first_visit:
                first_visit[node] = num_steps

            if loc in seen:
                # we'll revisit every other node within this cycle now, but how
                # long is the cycle?
                # all cycles seem to return to the starting node from the
                # terminating node, making this much  simpler
                cycle_length = num_steps - first_visit[node]
                cycles.append(cycle_length)
                break

            num_steps += 1
            seen.add(loc)

    # find the lowest common multiple between all cycle lengths, this will be
    # the first time they all land on the same node.
    # ...which happens to be the terminating node, so that's nice.
    res = math.lcm(*cycles)
    return res


def test_everything():
    assert part1(test_input) == 6

    test_input = """LR

    11A = (11B, XXX)
    11B = (XXX, 11Z)
    11Z = (11B, XXX)
    22A = (22B, XXX)
    22B = (22C, 22C)
    22C = (22Z, 22Z)
    22Z = (22B, 22B)
    XXX = (XXX, XXX)
    """.split(
        "\n"
    )

    assert part2(test_input) == 6


SOLUTION = Solutions(
    day=8,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=12737,
    part_2_answer=9064949303801,
)

if __name__ == "__main__":
    print(SOLUTION.part_1(), SOLUTION.part_1_solved)
    print(SOLUTION.part_2(), SOLUTION.part_2_solved)
