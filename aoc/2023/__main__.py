import sys
import time
from typing import TextIO

from solutions.solution import Solutions


def format_duration(duration: float) -> str:
    if duration > 0.1:
        return f"{duration:.2f}  s"
    if duration > 0.001:
        return f"{duration * 1_000:.2f} ms"
    if duration > 0.0000001:
        return f"{duration * 100_000:.2f} μs"

    return f"{duration:.2f} s"


def draw_table(solutions: list[Solutions], out: TextIO):
    max_name_length = 6
    max_part1_length = 10
    max_part2_length = 13
    part_1_header_length = max_part1_length + 5
    part_2_header_length = max_part2_length + 5
    max_time_length = 8
    max_length = (
        max_name_length
        + part_1_header_length
        + part_2_header_length
        + max_time_length
        + 11
    )
    out.write(f"╔{'═' * max_length}╗\n")
    out.write(f"║{'🐍 Advent of Code 2023 🐍'.center(max_length - 2)}║\n")
    out.write(
        "╠{}╦{}╦{}╦{}╣\n".format(
            "═" * (max_name_length + 2),
            "═" * (part_1_header_length + 2),
            "═" * (part_2_header_length + 2),
            "═" * (max_time_length + 2),
        )
    )
    out.write(
        "║{}║{}║{}║{}║\n".format(
            " Day ".ljust(max_name_length + 2),
            " Part 1 ".ljust(part_1_header_length + 2),
            " Part 2 ".ljust(part_2_header_length + 2),
            " Time ".ljust(max_time_length + 2),
        )
    )
    out.write(
        "╠{}╬{}╦{}╬{}╦{}╬{}╣\n".format(
            "═" * (max_name_length + 2),
            "═" * (max_part1_length + 2),
            "═" * 4,
            "═" * (max_part2_length + 2),
            "═" * 4,
            "═" * (max_time_length + 2),
        )
    )

    for solution in solutions:
        start = time.time()
        p1 = solution.part_1()
        p2 = solution.part_2()
        p1_symbol = "✅" if solution.part_1_solved else "❌"
        p2_symbol = "✅" if solution.part_2_solved else "❌"
        duration = format_duration(time.time() - start)

        out.write(
            "║ {} ║ {} ║ {} ║ {} ║ {} ║ {} ║\n".format(
                solution.name.ljust(max_name_length),
                str(p1).rjust(max_part1_length),
                p1_symbol,
                str(p2).rjust(max_part2_length),
                p2_symbol,
                str(duration).rjust(max_time_length),
            )
        )
        out.flush()

    out.write(
        "╚{}╩{}╩{}╩{}╩{}╩{}╝\n".format(
            "═" * (max_name_length + 2),
            "═" * (max_part1_length + 2),
            "═" * 4,
            "═" * (max_part2_length + 2),
            "═" * 4,
            "═" * (max_time_length + 2),
        )
    )


def write_table_to_buffer(out: TextIO):
    solutions = []

    for day in range(3, 25):
        try:
            mod = __import__("solutions", fromlist=[f"day{day}"])
            daily_mod = getattr(mod, f"day{day}")
            solutions.append(daily_mod.SOLUTION)
        except (ImportError, AttributeError):
            break

    draw_table(solutions, out)


def main(build_readme: bool = False):
    if build_readme:
        with open("README.md", "w", encoding="utf-8") as fout:
            fout.write("# Advent of Code 2023 \n\n")
            fout.write(
                "Decided to use python files over a notebook this year,"
                " experience is quite a bit nicer.\n\n"
            )

            fout.write("```\n")
            write_table_to_buffer(fout)
            fout.write("```\n")
    else:
        write_table_to_buffer(sys.stdout)


if __name__ == "__main__":
    build_readme = "readme" in sys.argv
    main(build_readme)