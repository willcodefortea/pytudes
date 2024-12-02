# Advent of Code CLI

Couple of utilities I use for Advent of Code.

## Installation

To install the CLI, simply check out this directory `pip install .` from this folder.

## How I use the CLI

First init a new solution

```console
aoc init <DAY>
```

This command will create a new solution file at the current directory with some initial setup in place, after that I begin running it:

```console
aoc run <DAY> --repeat
```

This will import the solution, run any tests, and output solutions to part 1 and part 2 with a sleep in between. Any changes to the source file will be picked up on the next run, and any new tests added too.

> Any function name that begins with `test_` is treated as a test. I tend to write two types, one to check behaviour against examples and another for bad results.

Once I've submitted solutions to Advent of Code, I'll run:

```console
aoc table
aoc create-readme
```

Which shows a friendly table of the results. Nothing really useful here, it just makes me happy.
