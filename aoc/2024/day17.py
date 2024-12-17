"""
Day 17: Chronospatial Computer

My program input was:

    2, 4, 1, 3, 7, 5, 0, 3, 1, 5, 4, 4, 5, 5, 3, 0

which can be rewritten as:

2,4 B = A % 8
1,3 B = B ^ 3
7,5 C = A / B ** 2
0,3 A = A / 2 ** 3
1,5 B = B ^ 5
4,4 B = B ^ C
5,5 OUT B % 8
3,0 RESTART if A == 0

Things we can notice:

    * B and C are overwritten therefore can be ignored
    * A is divided by 8
    * B % 8 is output, so only the trailing bytes matter

Rather than thinking of A as a decimal number, it's much clearer if we think of
it as base 8. In this case, A loses its least significant digit on every loop,
which means that lower significant digits can't contribute to the output for
the higher ones.

The test program is 6 characters long, and we're told that the result (in
decimal) is 117440. In base 8, this number is instead: 345300.

        8**5 8**4 8**3 8**2 8**1 8**0
Digits    3    4    5    3    0    0
Out       0    3    4    5    3    0 

So we want to search the digits in base 8, from higher order to lower, that
creates an output whos suffix matches the program, until we run out of 8 digits.Generator

Dfs to the rescue!
"""

from typing import Generator, Sequence, TypeVar, TypedDict

import aoc


class Registers(TypedDict):
    A: int
    B: int
    C: int


Program = list[int]
Data = tuple[Registers, Program]


def parse_input(_: Sequence[str]) -> Data:
    # eh, puzzle import is short today, just set it here
    registers: Registers = {"A": 55_593_699, "B": 0, "C": 0}
    program = [2, 4, 1, 3, 7, 5, 0, 3, 1, 5, 4, 4, 5, 5, 3, 0]

    return registers, program


def part_1(data: Data):
    registers, program = data
    out = _run_program(registers, program)
    return ",".join(map(str, out))


def part_2(data: Data):
    _, program = data
    MAX_BASE = len(program) - 1

    def dfs(register_a: int = 0, base: int = MAX_BASE, match_length=1) -> int:
        if match_length == len(program) + 1:
            # search past the max, so we must have a match!
            return register_a

        program_suffix = program[-match_length:]

        for offset in range(8):
            new_register_a = register_a + offset * 8**base

            registers: Registers = {"A": new_register_a, "B": 0, "C": 0}
            program_output = list(_run_program(registers, program))
            output_suffix = program_output[-match_length:]

            suffix_match = output_suffix == program_suffix
            if suffix_match:
                res = dfs(new_register_a, base - 1, match_length + 1)

                if res != -1:
                    return res
        return -1

    return dfs()


def _run_program(registers: Registers, program: Program) -> Generator[int, None, None]:
    instructions = list(_pairs(program))
    instruction_idx = 0
    value = 0
    while True:
        try:
            opcode, operand = instructions[instruction_idx]
        except IndexError:
            # halting condition
            return

        match operand:
            case 0 | 1 | 2 | 3:
                value = operand
            case 4:
                value = registers["A"]
            case 5:
                value = registers["B"]
            case 6:
                value = registers["C"]

        match opcode:
            case 0:
                registers["A"] = registers["A"] // 2**value
            case 1:
                registers["B"] = registers["B"] ^ operand
            case 2:
                registers["B"] = value % 8
            case 3:  # jmp
                if registers["A"] != 0:
                    instruction_idx = operand
                    continue
            case 4:
                registers["B"] = registers["B"] ^ registers["C"]
            case 5:
                yield value % 8
            case 6:
                registers["B"] = registers["A"] // 2**value
            case 7:
                registers["C"] = registers["A"] // 2**value

        instruction_idx += 1


T = TypeVar("T")


def _pairs(a_list: Sequence[T]):
    my_iter = iter(a_list)
    return zip(my_iter, my_iter)


SOLUTION = aoc.Solution(
    day=17,
    part_1=part_1,
    part_2=part_2,
    parse_data=parse_input,
    part_1_answer=-1,
    part_2_answer=-1,
)


def test_running_programs_1():
    registers: Registers = {"A": 0, "B": 0, "C": 9}
    list(_run_program(registers, [2, 6]))
    assert registers["B"] == 1


def test_running_programs_2():
    registers: Registers = {"A": 10, "B": 0, "C": 0}
    out = list(_run_program(registers, [5, 0, 5, 1, 5, 4]))
    assert out == [0, 1, 2]


def test_running_programs_3():
    registers: Registers = {"A": 2024, "B": 0, "C": 0}
    out = list(_run_program(registers, [0, 1, 5, 4, 3, 0]))
    assert out == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert registers["A"] == 0


def test_running_programs_4():
    registers: Registers = {"A": 0, "B": 29, "C": 0}
    list(_run_program(registers, [1, 7]))
    assert registers["B"] == 26


def test_running_programs_5():
    registers: Registers = {"A": 0, "B": 2024, "C": 43690}
    list(_run_program(registers, [4, 0]))
    assert registers["B"] == 44354


def test_part_1():
    registers: Registers = {"A": 729, "B": 0, "C": 0}
    out = list(_run_program(registers, [0, 1, 5, 4, 3, 0]))
    assert out == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]


def test_part_2():
    registers: Registers = {"A": 0, "B": 0, "C": 0}
    res = part_2((registers, [0, 3, 5, 4, 3, 0]))
    assert res == 117440
