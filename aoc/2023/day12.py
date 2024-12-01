from functools import cache
from typing import Sequence

from aoc import Solution

Data = list[tuple[str, tuple[int, ...]]]

test_data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".split(
    "\n"
)


def parse_input(lines: Sequence[str]) -> Data:
    out = []
    for line in lines:
        if not line:
            continue
        pattern, nums = line.split(" ")
        nums = tuple(int(n) for n in nums.split(","))
        out.append((pattern, nums))

    return out


@cache
def eat_the_string(
    pattern: str,
    damaged: tuple[int],
    current_block_length: int = 0,
) -> int:
    if not pattern:
        # no final block, so this is valid
        if len(damaged) == 0 and current_block_length == 0:
            return 1

        # is the last block the right length?
        if len(damaged) == 1 and damaged[0] == current_block_length:
            return 1

        # nope, not valid
        return 0

    n = 0
    maybe_broken = pattern[0] in "#?"
    if maybe_broken:
        # is broken or unknown, explore as if it's broken
        n += eat_the_string(pattern[1:], damaged, current_block_length + 1)

    maybe_fine = pattern[0] in ".?"
    if maybe_fine:
        # is not broken or unknown, explore as if not broken
        if damaged and damaged[0] == current_block_length:
            # explore as if this damage block is complete
            n += eat_the_string(pattern[1:], damaged[1:])
        elif current_block_length == 0:
            n += eat_the_string(pattern[1:], damaged)
    return n


def unfold(pattern: str, damaged: tuple[int, ...]) -> tuple[str, tuple[int, ...]]:
    return "?".join([pattern] * 5), damaged * 5


def part_1(data: Data):
    # we add a valid node at the end of the pattern to make end case easier to find
    return sum(eat_the_string(pattern, damaged) for pattern, damaged in data)


def part_2(data: Data):
    unfolded = [unfold(pattern, damaged) for pattern, damaged in data]
    return part_1(unfolded)


SOLUTION = Solution(
    day=12,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=7173,
    part_2_answer=29826669191291,
)


class Tests:
    DATA = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".split(
        "\n"
    )

    def test_simple_arrangements(self):
        assert eat_the_string("???.###", (1, 1, 3)) == 1

    def test_part_1(self):
        assert part_1(parse_input(self.DATA)) == 21

    def test_unfolding(self):
        assert unfold(".#", (1,)) == (".#?.#?.#?.#?.#", (1, 1, 1, 1, 1))

    def test_part_2_simple(self):
        assert part_2([(".??..??...?##.", (1, 1, 3))]) == 16384


if __name__ == "__main__":
    print(SOLUTION.part_1(), SOLUTION.part_1_solved)
    print(SOLUTION.part_2(), SOLUTION.part_2_solved)
