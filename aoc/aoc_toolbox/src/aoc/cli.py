import os
import re
import shutil
import sys
import time
from datetime import date
from pathlib import Path
from typing import TextIO

import click
from aoc.solution import Solution

cwd = os.getcwd()


@click.group()
def cli():
    pass


@cli.command(help="Run a solution for a given day")
@click.argument("day", type=int, required=True)
def run(day: int):
    sys.path.append(cwd)
    try:
        mod = __import__(f"day{day:>02}")
    except ModuleNotFoundError:
        click.echo(
            f"No solution found in current directory, run: aoc init {day}", err=True
        )
        click.get_current_context().exit(1)
    solution: Solution = mod.SOLUTION
    click.echo(f"Part 1: {solution.part_1()}")
    click.echo(f"Part 2: {solution.part_2()}")


@cli.command(help="Creates a template for a solutions")
@click.argument("day", type=int, required=True)
@click.option("--force", type=bool, is_flag=True)
def init(day: int, force: bool = False):
    click.echo(f"Initialising day {day} in current directory")
    template_path = Path(__file__).parent / "day_n.py"

    solution_path = Path(cwd) / f"day{day:>02}.py"
    data_path = Path(cwd) / f"day{day:>02}.txt"

    if solution_path.exists() and not force:
        click.echo("Solution file already exists, aborting", err=True)
        click.get_current_context().exit(1)

    shutil.copy(template_path, solution_path)
    data_path.touch()


@cli.command()
@click.option("--all", type=bool, is_flag=True)
@click.option(
    "--year",
    type=int,
    help="What year are the solutions for?",
    required=False,
    default=date.today().year,
)
def table(all: bool, year: int):
    sys.path.append(cwd)
    solution_files = [f for f in os.listdir(".") if re.match(r"day\d\d\.py", f)]
    _write_table_to_buffer(sys.stdout, year, 25 if all else len(solution_files))


@cli.command()
@click.option(
    "--year",
    type=int,
    help="What year are the solutions for?",
    required=False,
    default=date.today().year,
)
def create_readme(year: int):
    sys.path.append(cwd)
    with open("README.md", "w", encoding="utf-8") as fout:
        fout.write(f"# Advent of Code {year} \n\n")
        fout.write("All files are designed to be ran with my AoC toolbox CLI.\n\n")

        fout.write("```txt\n")
        _write_table_to_buffer(fout, year)
        fout.write("```\n")

        fout.write("\n\n")
        fout.write("_Generated by `aoc create-readme`._\n")
        fout.write("This table renders nicer on the console, honest.\n")


def _format_duration(duration: float) -> str:
    if duration > 0.1:
        return f"{duration:.2f}  s"
    if duration > 0.001:
        return f"{duration * 1_000:.2f} ms"
    if duration > 0.0000001:
        return f"{duration * 100_000:.2f} μs"

    return f"{duration:.2f} s"


def _draw_table(solutions: list[Solution], out: TextIO, year: int):
    max_name_length = 6
    max_part1_length = 10
    max_part2_length = 15
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
    title = f"🐍 Advent of Code {year} 🐍"
    out.write(f"║{title.center(max_length - 2)}║\n")
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
            " Day ".center(max_name_length + 2),
            " Part 1 ".center(part_1_header_length + 2),
            " Part 2 ".center(part_2_header_length + 2),
            " Time ".center(max_time_length + 2),
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

    total_time = 0

    for solution in solutions:
        start = time.time()
        p1 = solution.part_1()
        p2 = solution.part_2()
        p1_symbol = "✅" if solution.part_1_solved else "❌"
        p2_symbol = "✅" if solution.part_2_solved else "❌"

        duration = time.time() - start
        total_time += duration

        out.write(
            "║ {} ║ {} ║ {} ║ {} ║ {} ║ {} ║\n".format(
                solution.name.ljust(max_name_length),
                str(p1).rjust(max_part1_length),
                p1_symbol,
                str(p2).rjust(max_part2_length),
                p2_symbol,
                _format_duration(duration).rjust(max_time_length),
            )
        )
        out.flush()

    out.write(
        "╚{}╩{}╩{}╩{}╩{}╬{}╣\n".format(
            "═" * (max_name_length + 2),
            "═" * (max_part1_length + 2),
            "═" * 4,
            "═" * (max_part2_length + 2),
            "═" * 4,
            "═" * (max_time_length + 2),
        )
    )
    out.write(
        " {} {} {} {} {}║ {} ║\n".format(
            " " * (max_name_length + 2),
            " " * (max_part1_length + 2),
            " " * 4,
            " " * (max_part2_length + 2),
            " " * 4,
            _format_duration(total_time).rjust(max_time_length),
        )
    )
    out.write(
        " {} {} {} {} {}╚{}╝\n".format(
            " " * (max_name_length + 2),
            " " * (max_part1_length + 2),
            " " * 4,
            " " * (max_part2_length + 2),
            " " * 4,
            "═" * (max_time_length + 2),
        )
    )


def _write_table_to_buffer(out: TextIO, year: int, num_days: int = 25):
    solutions = []

    for day in range(1, num_days + 1):
        try:
            daily_mod = __import__(f"day{day:>02}")
            solutions.append(daily_mod.SOLUTION)
        except (ImportError, AttributeError):
            solutions.append(
                Solution(
                    day=day,
                    part_1_answer=0,
                    part_1=lambda _: -1,
                    part_2_answer=0,
                    part_2=lambda _: -1,
                    parse_data=lambda _: _,
                )
            )

    _draw_table(solutions, out, year)
