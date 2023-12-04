import re

test_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


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


def part_1(lines: list[str], winning_length: int):
    all_cards = parse_input(lines, winning_length)

    total = 0
    for _, winning, cards in all_cards:
        total += score_hand(winning, cards)

    return total


assert part_1(test_input.split("\n"), 5) == 13

data = open("day4.txt").read()
print(part_1(data.split("\n"), 10))


def part_2(lines: list[str], winning_length: int):
    all_cards = parse_input(lines, winning_length)

    to_process = all_cards[:]
    processed = 0

    while to_process:
        card_num, winning, hand = to_process.pop()
        num_matching = len(set(winning) & set(hand))
        to_process.extend(all_cards[card_num : card_num + num_matching])
        processed += 1

    return processed


def part_2_dynamic(lines: list[str], winning_length: int):
    all_cards = parse_input(lines, winning_length)

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


assert part_2_dynamic(test_input.split("\n"), 5) == 30
print(part_2(data.split("\n"), 10))
