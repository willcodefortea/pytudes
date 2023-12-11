test_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".split(
    "\n"
)


def mapt(f, l):
    return tuple(map(f, l))


def parse_input(lines: list[str]):
    out: list[list[int]] = []
    for line in lines:
        if not line:
            continue
        out.append([int(x) for x in line.split(" ")])

    return out


def extrapolate_value(vals: tuple[int]) -> int:
    if not any(vals):
        return 0

    distances: list[int] = []

    stack = list(vals[:1])
    for n in vals[1:]:
        distances.append(n - stack[-1])
        stack.append(n)

    return vals[-1] + extrapolate_value(distances)


def part1(lines: list[str]):
    vals = parse_input(lines)
    return sum(extrapolate_value(v) for v in vals)


def part2(lines: list[str]):
    vals = parse_input(lines)
    return sum(extrapolate_value(v[::-1]) for v in vals)


class Tests:
    def test_parse_input(self):
        assert parse_input(test_input)[0] == [0, 3, 6, 9, 12, 15]

    def test_extrapolate_all_zero_is_zero(self):
        assert extrapolate_value((0, 0, 0)) == 0

    def test_extrapolate_all_3s_is_3(self):
        assert extrapolate_value((3, 3, 3)) == 3

    def test_extrapolate_full(self):
        assert extrapolate_value((0, 3, 6, 9, 12, 15)) == 18

    def test_part1(self):
        assert part1(test_input) == 114

    def test_extrapoloate_backwards(self):
        assert extrapolate_value([10, 13, 16, 21, 30, 45][::-1]) == 5

    def test_part2(self):
        assert part2(test_input) == 2


data = open("day9.txt").read().split("\n")
print("Part 1:", part1(data))
print("Part 2:", part2(data))
