"""
Day 4: Ceres Search

Not super happy with the first part of this! Python's negative
indexing messed me up when searching diagnoals. I explored 
pulling out each diagonal in a smiliar way to the verticals,
and there's no real need to do so, given the size of the data 
set.
"""

import re
from typing import Sequence

import aoc

Data = Sequence[str]


def parse_input(lines: Sequence[str]) -> Data:
    return [line for line in lines if line]


def part_1(data: Data):
    total = 0
    # horizontal
    for line in data:
        total += len(re.findall("XMAS", line + "|" + line[::-1]))

    # vertical
    transposed = []
    for x in range(len(data)):
        line = "".join(line[x] for line in data)
        transposed.append(line)

    for line in transposed:
        total += len(re.findall("XMAS", line + "|" + line[::-1]))

    # diagonals
    # just check each diagonal fanning out from each point
    for y in range(len(data)):
        for x in range(len(data[0])):
            directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))
            for dx, dy in directions:
                try:
                    line = ""
                    # negative indexing caused issues for me here
                    for i in range(4):
                        ny = y + dy * i
                        nx = x + dx * i
                        if ny < 0 or nx < 0:
                            break
                        line += data[ny][nx]
                except IndexError:
                    continue
                total += line == "XMAS"

    return total


def part_2(data: Data):
    total = 0
    for y in range(1, len(data) - 1):
        for x in range(1, len(data[0]) - 1):
            left = data[y - 1][x - 1] + data[y][x] + data[y + 1][x + 1]
            right = data[y + 1][x - 1] + data[y][x] + data[y - 1][x + 1]

            total += (left == "SAM" or left == "MAS") and (
                right == "SAM" or right == "MAS"
            )

    return total


SOLUTION = aoc.Solution(
    day=4,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=2603,
    part_2_answer=1965,
)


def test_part_1():
    lines = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".split(
        "\n"
    )
    assert part_1(lines) == 18


def test_part_2():
    lines = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".split(
        "\n"
    )
    assert part_2(lines) == 9
