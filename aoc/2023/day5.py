import re
from typing import Callable

from solution import Solutions

test_data = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".split(
    "\n"
)


def mapt(a_list: list, f: Callable):
    return tuple(f(x) for x in a_list)


def parse_data(lines: list[str]):
    seeds = []
    maps = []

    for line in lines:
        if line.startswith("seeds"):
            seeds = mapt(re.findall(f"\d+", line), int)
        elif "to" in line:
            maps.append([])
        elif line:
            destination, origin, length = mapt(line.split(" "), int)
            maps[-1].append((origin, destination, length))

    # we always process in order, so sort now
    for mapping in maps:
        mapping.sort()

    return seeds, maps


def part_1(data):
    seeds, maps = data
    final_locations = []

    for seed in seeds:
        loc = seed
        for mapping in maps:
            for src, dest, size in mapping:
                if src <= loc < src + size:
                    loc = dest + (loc - src)
                    break

        final_locations.append(loc)
    return min(final_locations)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def part_2(data):
    seeds, maps = data
    all_lowest = []

    ranges = []
    for seed, length in chunks(seeds, 2):
        ranges.append((seed, seed + length - 1))

    for mapping in maps:
        destination_ranges = []
        while ranges:
            range_lo, range_hi = ranges.pop()
            for src, dest, length in mapping:
                starts_within_mapping = src <= range_lo < src + length
                ends_within_mapping = src <= range_hi < src + length

                if starts_within_mapping:
                    if ends_within_mapping:
                        # range is entirely within this mapping
                        destination_ranges.append(
                            (dest + range_lo - src, dest + range_hi - src)
                        )
                    else:
                        # range extends beyond this mapping, so add the that
                        # fits to the destinations...
                        destination_ranges.append(
                            (dest + range_lo - src, dest + length - 1)
                        )
                        # ...and the bit that runs over the edge of this mapping
                        # to explore
                        ranges.append((src + length, range_hi))
                    break

                if ends_within_mapping:
                    # range started before this mapping, so pass through the
                    # bit that started outside it...
                    destination_ranges.append((range_lo, src - 1))
                    # ...and explore the remaining bit of the range
                    ranges.append((src, range_hi))
                    break
            else:
                # we exited without breaking, there was never an overlap with
                # a mapping, so just pass through
                destination_ranges.append((range_lo, range_hi))

        # move to the next set of ranges
        ranges = destination_ranges
        all_lowest.append(min(start for start, _ in destination_ranges))

    return all_lowest[-1]


SOLUTION = Solutions(
    day=5,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_data,
    part_1_answer=579439039,
    part_2_answer=7873084,
)

if __name__ == "__main__":
    print(SOLUTION.part_1(), SOLUTION.part_1_solved)
    print(SOLUTION.part_2(), SOLUTION.part_2_solved)
