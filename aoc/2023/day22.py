import re
from collections import namedtuple

from aoc import Solution

Brick = namedtuple("B", "start,end")
Data = list[Brick]


def parse_input(lines: list[str]) -> Data:
    bricks: list[Brick] = []
    for line in lines:
        if not line:
            continue
        nums = [int(n) for n in re.findall(r"\d+", line)]
        start = nums[:3]
        end = nums[3:]
        bricks.append(Brick(start, end))
    return bricks


def overlapping_xy(a: Brick, b: Brick):
    x_plane = a.start.x <= b.end.x and a.end.x >= b.start.x
    y_plane = a.start.y <= b.end.y and a.end.y >= b.start.y
    return x_plane and y_plane


def overlapping(a: Brick, b: Brick):
    x_plane = a.start.x <= b.end.x and a.end.x >= b.start.x
    y_plane = a.start.y <= b.end.y and a.end.y >= b.start.y
    z_plane = a.start.z <= b.end.z and a.end.z >= b.start.z
    return x_plane and y_plane and z_plane


def supporting(a: Brick, b: Brick):
    z_plane = max(a.start.z, a.end.z) == min(b.start.z, b.end.z) - 1
    return overlapping_xy(a, b) and z_plane


def fall(bricks: Data, in_place: bool | None = None, remove: Brick | None = None):
    max_heights = {}
    n_fell = 0
    for brick in bricks:
        if brick == remove:
            continue

        x0, y0, z0 = brick.start
        x1, y1, z1 = brick.end

        xy_plane = [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
        height = max(max_heights.get(p, 0) for p in xy_plane)
        drop = z0 - height - 1
        if drop:
            n_fell += 1
            z1 -= drop
            if in_place:
                brick.start[2] -= drop
                brick.end[2] -= drop

        for p in xy_plane:
            max_heights[p] = z1

    return n_fell


def part_1(data: Data):
    bricks = sorted(data, key=lambda b: b.end[2])
    fall(bricks, in_place=True)
    return sum(fall(bricks, remove=brick) == 0 for brick in bricks)


def part_2(data: Data):
    bricks = sorted(data, key=lambda b: b.end[2])
    fall(bricks, in_place=True)
    return sum(fall(bricks, remove=brick) for brick in bricks)


SOLUTION = Solution(
    day=22,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=401,
    part_2_answer=63491,
)


class Test:
    DATA = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
""".split(
        "\n"
    )

    def test_part_1(self):
        assert part_1(parse_input(self.DATA)) == 5

    def test_part_2(self):
        assert part_2(parse_input(self.DATA)) == 7


if __name__ == "__main__":
    print(SOLUTION.part_1())
    print(SOLUTION.part_2())
