import re

test_input = """Time:      7  15   30
Distance:  9  40  200""".split(
    "\n"
)


def parse_input(lines: list[str]):
    times = map(int, re.findall("\d+", lines[0]))
    distances = map(int, re.findall("\d+", lines[1]))

    return list(zip(times, distances))


def part_1(lines: list[str]):
    races = parse_input(lines)

    res = 1
    for time, distance in races:
        res *= num_winning_options(time, distance)

    return res


def num_winning_options(time: int, distance: int) -> int:
    res = 0
    for t in range(time):
        if t * (time - t) > distance:
            res += 1
    return res


def part_2(lines: list[str]):
    races = parse_input(lines)
    times, distances = zip(*races)
    time = int("".join(str(x) for x in times))
    distance = int("".join(str(x) for x in distances))

    return num_winning_options(time, distance)


data = open("day6.txt").read().split("\n")
assert part_1(test_input) == 288
print("Part 1: ", part_1(data))

assert part_2(test_input) == 71503
print("Part 2: ", part_2(data))
