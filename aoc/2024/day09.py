"""
Day 9: Disk Fragmenter

This one took me a good 10 minutes just to understand the question!

For the first part, I did a two-cursor approach, one going forward and one going
backwards. The idea being the first would keep track of the free space, and the
one from the end would track the file being worked on.

The empty space is then swapped with the file.

  0..111....22222
   ^            ^
  02.111....2222.
    ^          ^
  022111....222..
        ^     ^

etc.

The second part can't be solved like this, as we need to act on entire blocks,
not just single cells. My initial solution took around 6s, and that involved
lots of insertions and deletions.

Instead we see that we're never adding any blocks we care about, any newly
created space from files moving will never be used by another file (as that
would mean they move right), so we can just focus on shrinking the free space a
file moves into.

This took the solution from 5/6s to 1.1s to run. Deleting empty spaces cut that
to 0.8s. \o/

There's probably a way to do even better by considering blocks, rather than
individual cells, but that'll do for now.
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
    free_list = []
    file_list = []
    offset = 0

    for i, val in enumerate(data):
        is_free_space = i % 2 == 1

        if is_free_space:
            free_list.append((offset, val))
            char = None
        else:
            file_list.append((offset, file_id, val))
            char = file_id
            file_id += 1

        offset += val
        for _ in range(val):
            disk.append(char)

    for file_start, file_id, file_size in reversed(file_list):
        for space_idx, (space_start, space_size) in enumerate(free_list):
            if space_size >= file_size and space_start < file_start:
                for i in range(file_size):
                    disk[space_start + i] = file_id
                    disk[file_start + i] = None
                free_list[space_idx] = (space_start + file_size, space_size - file_size)
                if space_size == file_size:
                    del free_list[space_idx]
                else:
                    free_list[space_idx] = (
                        space_start + file_size,
                        space_size - file_size,
                    )
                break

    checksum = 0
    for i, file_id in enumerate(disk):
        if file_id:
            checksum += i * file_id
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
