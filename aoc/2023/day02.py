from collections import defaultdict

from aoc import Solution

Games = tuple[int, list[dict[str, int]]]


def parse_input(lines: list[str]) -> list[Games]:
    return [parse_game(line) for line in lines if line]


def parse_game(line: str) -> Games:
    # line:
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    game_id_raw, rounds = line.split(":")

    game_id = int(game_id_raw.split(" ")[1])

    parsed_rounds = []

    for round in rounds.split(";"):
        current_round = defaultdict(int)
        for cubes in round.split(","):
            num, colour = cubes.strip().split(" ")
            current_round[colour] = int(num)

        parsed_rounds.append(current_round)

    return game_id, parsed_rounds


def part_1(games: list[Games]) -> int:
    total = 0

    for game in games:
        game_id, rounds = game

        for round in rounds:
            if round["blue"] > 14 or round["red"] > 12 or round["green"] > 13:
                break

        else:
            total += game_id

    return total


def part_2(games: list[Games]) -> int:
    total = 0

    for game in games:
        _, rounds = game

        max_red = 0
        max_green = 0
        max_blue = 0

        for round in rounds:
            max_red = max(max_red, round["red"])
            max_blue = max(max_blue, round["blue"])
            max_green = max(max_green, round["green"])

        power = max_red * max_green * max_blue

        total += power

    return total


SOLUTION = Solution(
    day=2,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=2369,
    part_2_answer=66363,
)

if __name__ == "__main__":
    print(SOLUTION.part_1())
    print(SOLUTION.part_2())
