from typing import Callable

from solution import Solutions

Data = list[str]


def parse_input(lines: list[str]) -> Data:
    return [l for l in lines if l]


def digits_only(s: str) -> list[str]:
    return "".join([c for c in s if c in "0123456789"])


def digits_only_replace_words(s: str) -> list[str]:
    num_words = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

    old_s = s
    for pos in range(len(old_s)):
        for number, word in enumerate(num_words, 1):
            if old_s[pos:].startswith(word):
                s = s.replace(word, str(number), 1)

    return "".join([c for c in s if c in "0123456789"])


def calibration_value(s: str, clean: Callable[[str], str]) -> int:
    digits = clean(s)
    return int(digits[0] + digits[-1])


def part_1(data: Data):
    return sum(calibration_value(line, digits_only) for line in data)


def part_2(data: Data):
    return sum(calibration_value(line, digits_only_replace_words) for line in data)


SOLUTION = Solutions(
    day=1,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=53334,
    part_2_answer=52834,
)

if __name__ == "__main__":
    print(
        SOLUTION.part_1(),
    )
    print(
        SOLUTION.part_2(),
    )
