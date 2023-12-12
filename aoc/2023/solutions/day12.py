from solution import Solutions

Data = list[tuple[str, list[int]]]

test_data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".split(
    "\n"
)


def parse_input(lines: list[str]) -> Data:
    out = []
    for line in lines:
        if not line:
            continue
        pattern, nums = line.split(" ")
        nums = [int(n) for n in nums.split(",")]
        out.append((pattern, nums))

    return out


def is_valid(pattern: str, damaged: list[int]) -> bool:
    if "?" in pattern:
        return False
    damaged_chunk_len = [len(c) for c in pattern.split(".") if c]
    return damaged_chunk_len == damaged


def num_arrangements(pattern: str, damaged: list[int]) -> int:
    chars = list(pattern)

    total = 0
    # DFS brute force, see if it works!
    for idx, char in enumerate(chars):
        if char != "?":
            continue

        for c in ".#":
            # branch, try different values
            test_pattern = chars[:]
            test_pattern[idx] = c
            total += num_arrangements("".join(test_pattern), damaged)
        # we've made a change, other branches will explore the remaining patterns
        break

    total += int(is_valid(pattern, damaged))
    return total


def part_1(data: Data):
    return sum(num_arrangements(pattern, damaged) for pattern, damaged in data)


def part_2(data: Data):
    return None


SOLUTION = Solutions(
    day=12,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=7173,
    part_2_answer=0,
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

    def test_is_valid(self):
        assert is_valid("#.#.###", [1, 1, 3])
        assert not is_valid("##..###", [1, 1, 1])

    def test_simple_arrangements(self):
        assert num_arrangements("???.###", [1, 1, 3]) == 1

    def test_part_1(self):
        assert part_1(parse_input(self.DATA)) == 21

    def test_unfolding(self):
        assert unfold(".#", [1]) == (".#?.#?.#?.#?.#", [1, 1, 1, 1, 1])

    def test_part_2_simple(self):
        assert part_1([(".??..??...?##.", [1, 1, 3])]) == 16384


if __name__ == "__main__":
    print(SOLUTION.part_1(), SOLUTION.part_1_solved)
    print(SOLUTION.part_2(), SOLUTION.part_2_solved)
