from collections import Counter
from functools import cmp_to_key, partial

test_data = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".split(
    "\n"
)

CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

Hand = tuple[str, int]


def parse_input(lines: list[str]):
    results = []
    for line in lines:
        if not line:
            continue
        hand, bid = line.split(" ")
        results.append((hand, int(bid)))
    return results


def score_hand(hand: str):
    counts = Counter(hand)
    card_counts = sorted(counts.values(), reverse=True)
    match card_counts:
        case (5,):
            return FIVE_OF_A_KIND
        case (4, 1):
            return FOUR_OF_A_KIND
        case (3, 2):
            return FULL_HOUSE
        case (3, 1, 1):
            return THREE_OF_A_KIND
        case (2, 2, 1):
            return TWO_PAIR
        case (2, 1, 1, 1):
            return ONE_PAIR
        case _:
            return HIGH_CARD


def compare_hands(hand1: str, hand2: str, convert_jokers: bool = False):
    original_hand1 = hand1
    original_hand2 = hand2
    card_rankings = CARDS[:]

    if convert_jokers:
        hand1 = convert_jokers_to_highest(hand1)
        hand2 = convert_jokers_to_highest(hand2)
        # move jokers to weakest position
        card_rankings.remove("J")
        card_rankings.append("J")

    hand1_score = score_hand(hand1)
    hand2_score = score_hand(hand2)

    if hand1_score > hand2_score:
        return True
    if hand1_score < hand2_score:
        return False

    for card1, card2 in zip(original_hand1, original_hand2):
        if card1 != card2:
            return card_rankings.index(card1) < card_rankings.index(card2)
    return False


def convert_jokers_to_highest(hand: str) -> str:
    if "J" not in hand:
        return hand

    # we only need to try cards already in the hand, but make sure we don't
    # readd jokers
    cards_to_try = set(hand)
    cards_to_try.remove("J")
    # edge case, if all jokers then make sure we try highest ranked cards
    if len(cards_to_try) == 0:
        cards_to_try.add(CARDS[0])
    new_hands = [hand.replace("J", card) for card in cards_to_try]
    winning = max(new_hands, key=cmp_to_key(compare_hands))
    return winning


def compare_hand_bid(hand1: Hand, hand2: Hand, convert_jokers: bool = False):
    return 1 if compare_hands(hand1[0], hand2[0], convert_jokers) else -1


def part_1(lines: list[str]):
    hands = parse_input(lines)

    sorted_hands = sorted(hands, key=cmp_to_key(compare_hand_bid))
    res = 0
    for indx, (c, bid) in enumerate(sorted_hands, start=1):
        res += indx * bid
    return res


def part_2(lines: list[str]):
    hands = parse_input(lines)

    cmp = partial(compare_hand_bid, convert_jokers=True)
    sorted_hands = sorted(hands, key=cmp_to_key(cmp))
    res = 0
    for indx, (_, bid) in enumerate(sorted_hands, start=1):
        res += indx * bid
    return res


assert score_hand("AAAAA") == FIVE_OF_A_KIND
assert score_hand("AA8AA") == FOUR_OF_A_KIND
assert score_hand("23332") == FULL_HOUSE
assert score_hand("TTT98") == THREE_OF_A_KIND
assert score_hand("23432") == TWO_PAIR
assert score_hand("A23A4") == ONE_PAIR
assert compare_hands("AAAAA", "AA8AA")
assert not compare_hands("AA8AA", "AAAAA")
assert compare_hands("77888", "77788")


data = open("day7.txt").read().split("\n")
assert part_1(test_data) == 6440
print("Part 1:", part_1(data))

assert part_2(test_data) == 5905
print("Part 2:", part_2(data))
