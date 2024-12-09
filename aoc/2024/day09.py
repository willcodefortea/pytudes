"""
Day 9: Disk Fragmenter

This one took me a good 10 minutes just to understand the question!

For the first part, I did a two-cursor approach, one going forward
and one going backwards. The idea being the first would keep track
of the free space, and the one from the end would track the file
being worked on.

The empty space is then swapped with the file.

  0..111....22222
   ^            ^
  02.111....2222.
    ^          ^
  022111....222..
        ^     ^

etc.

The second part can't be solved like this, as we need to act on
entire blocks, not just single cells. 
"""

from typing import Sequence

import aoc

Data = list[int]


def parse_input(lines: Sequence[str]) -> Data:
    return [int(c) for c in lines[0]]


def part_1(data: Data):
    disk = []
    file_id = 0

    # expand the disk
    for i, val in enumerate(data):
        is_free_space = i % 2 == 1

        if is_free_space:
            disk.extend([None] * val)
        else:
            disk.extend([file_id] * val)
            file_id += 1

    # initialise curosrs
    cursor = 0
    end_cursor = len(disk) - 1

    while cursor < end_cursor:
        while disk[cursor] is not None:
            cursor += 1

        if cursor < end_cursor:
            disk[cursor] = disk[end_cursor]
            disk[end_cursor] = None

        while disk[end_cursor] is None:
            end_cursor -= 1

    checksum = sum(idx * val for idx, val in enumerate(disk) if val)
    return checksum


def part_2(data: Data):
    disk = []
    file_id = 0

    for i, val in enumerate(data):
        is_free_space = i % 2 == 1

        if is_free_space:
            disk.append((None, val))
        else:
            disk.append((file_id, val))
            file_id += 1

    processed = set()
    for _ in range(len(data) // 2):
        data_offset, (file_id, file_size) = next(
            (i, b)
            for i, b in enumerate(disk[::-1])
            if b[0] is not None and b[0] not in processed
        )
        data_idx = len(disk) - data_offset - 1
        empty_blocks = ((i, b) for i, b in enumerate(disk) if b[0] is None)

        for idx, (_, empty_size) in empty_blocks:
            if idx > data_idx:
                continue
            remaining = empty_size - file_size
            if remaining == 0:
                disk[idx] = (file_id, file_size)
                disk[data_idx] = (None, empty_size)
                break
            elif remaining > 0:
                disk[idx] = (file_id, file_size)
                disk[data_idx] = (None, file_size)
                disk.insert(idx + 1, (None, remaining))
                break

        processed.add(file_id)

    checksum = 0
    offset = 0
    for file_id, size in disk:
        if file_id:
            for i in range(size):
                checksum += (offset + i) * file_id
        offset += size
    return checksum


SOLUTION = aoc.Solution(
    day=9,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=6279058075753,
    part_2_answer=6301361958738,
)


def test_part_1():
    test_input = "2333133121414131402".split("\n")
    data = parse_input(test_input)
    assert part_1(data) == 1928


def test_part_2():
    test_input = "2333133121414131402".split("\n")
    data = parse_input(test_input)
    assert part_2(data) == 2858
