from typing import NamedTuple, Tuple, List
import sys

NORTH = 1j
EAST = 1
SOUTH = -1j
WEST = -1

HEADING_TO_STR = {NORTH: "N", EAST: "E", SOUTH: "S", WEST: "W"}

Heading = complex
Position = complex
PlatueSize = Tuple[int, int]
Obsticles = List[complex]


class Rover(NamedTuple):
    heading: Heading
    position: Position


def turn_left(heading: Heading) -> Heading:
    return heading * 1j


def turn_right(heading: Heading) -> Heading:
    return heading * -1j


def move(position: Position, heading: Heading, plateu_size: PlatueSize) -> Position:
    new_position = position + heading
    return complex(
        new_position.real % plateu_size[0], new_position.imag % plateu_size[1]
    )


def turn_rover_left(rover: Rover) -> Rover:
    return Rover(position=rover.position, heading=turn_left(rover.heading))


def turn_rover_right(rover: Rover) -> Rover:
    return Rover(position=rover.position, heading=turn_right(rover.heading))


def move_rover(rover: Rover, platue_size: PlatueSize) -> Rover:
    return Rover(
        position=move(rover.position, rover.heading, platue_size), heading=rover.heading
    )


def perform_command(cmd: str, rover: Rover, plateu_size: PlatueSize) -> Rover:
    if cmd == "L":
        return turn_rover_left(rover)
    elif cmd == "R":
        return turn_rover_right(rover)
    elif cmd == "M":
        return move_rover(rover, plateu_size)
    else:
        raise Exception(f"Unknown command {cmd}")


def execute(
    commands: str,
    plateu_size: PlatueSize = (10, 10),
    obsticles: Obsticles = [],
) -> str:
    rover = Rover(position=0, heading=NORTH)
    hit_obsticle = False
    for cmd in commands:
        new_rover = perform_command(cmd, rover, plateu_size)
        if new_rover.position in obsticles:
            hit_obsticle = True
            break
        rover = new_rover

    return rover_as_string(rover, hit_obsticle)


def rover_as_string(rover: Rover, hit_obsticle: bool) -> str:
    pos_x = int(rover.position.real)
    pos_y = int(rover.position.imag)
    heading_str = HEADING_TO_STR[rover.heading]

    rover_str = f"{pos_x}:{pos_y}:{heading_str}"
    if hit_obsticle:
        rover_str = f"O:{rover_str}"
    return rover_str


if __name__ == "__main__":
    commands = sys.argv[1]
    print(execute(commands))
