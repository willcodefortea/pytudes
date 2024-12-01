import re
from functools import partial

from aoc import Solution


def parse_input(lines: list[str], winning_length: int):
    all_cards = []
    for line in lines:
        if not line:
            continue
        nums = [int(c) for c in re.findall(r"\d+", line)]
        card_num = nums[0]
        winning = nums[1 : winning_length + 1]
        cards = nums[winning_length + 1 :]

        all_cards.append((card_num, winning, cards))

    return all_cards


def score_hand(winning: list[str], hand: list[str]) -> int:
    points = 0

    for card in hand:
        if card in winning:
            if points == 0:
                points = 1
            else:
                points *= 2

    return points


def part_1(all_cards):
    total = 0
    for _, winning, cards in all_cards:
        total += score_hand(winning, cards)

    return total


def part_2(all_cards):
    to_process = all_cards[:]
    processed = 0

    while to_process:
        card_num, winning, hand = to_process.pop()
        num_matching = len(set(winning) & set(hand))
        to_process.extend(all_cards[card_num : card_num + num_matching])
        processed += 1

    return processed


def part_2_dynamic(all_cards):
    # array of 1s as each card is processed at least once
    processing_vals = [1] * len(all_cards)

    # iterate in reverse order, each card adds ones after it so if we know how
    # much they contribute before we need them then we can answer instantly
    for card_num, winning, hand in all_cards[::-1]:
        idx = card_num - 1
        num_matching = len(set(winning) & set(hand))
        # each card is processed + each one after for the number of matches
        processing_vals[idx] = sum(processing_vals[idx : idx + 1 + num_matching])
    return sum(processing_vals)


SOLUTION = Solution(
    day=4,
    part_1=part_1,
    part_2=part_2_dynamic,
    parse_data=partial(parse_input, winning_length=10),
    part_1_answer=20117,
    part_2_answer=13768818,
)

if __name__ == "__main__":
    print(SOLUTION.part_1(), SOLUTION.part_1_solved)
    print(SOLUTION.part_2(), SOLUTION.part_2_solved)
