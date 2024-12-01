import os
from typing import Callable, Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class Solution(Generic[R]):
    def __init__(
        self,
        *,
        part_1: Callable[[T], R],
        part_2: Callable[[T], R],
        parse_data: Callable[[list[str]], T],
        day: int,
        part_1_answer: R | None = None,
        part_2_answer: R | None = None,
    ):
        self._day = day

        self._parse_data = parse_data
        self._data = parse_data(self._read_input())
        self._part_1 = part_1
        self._part_2 = part_2
        self._part_1_answer = part_1_answer
        self._part_2_answer = part_2_answer

        self._part_1_solution = None
        self._part_2_solution = None

    def _read_input(self):
        path = f"day{self._day:>02}.txt"
        try:
            with open(path, "r", encoding="utf-8") as fin:
                return fin.read().split("\n")
        except FileNotFoundError:
            return []

    @property
    def data(self):
        if not self._data:
            self._data = self._parse_data(self._read_input())
        return self._data

    def part_1(self) -> R:
        if self._part_1_solution is None:
            self._part_1_solution = self._part_1(self.data)
        return self._part_1_solution

    def part_2(self) -> R:
        if self._part_2_solution is None:
            self._part_2_solution = self._part_2(self.data)
        return self._part_2_solution

    @property
    def part_1_solved(self):
        return self.part_1() == self._part_1_answer

    @property
    def part_2_solved(self):
        return self.part_2() == self._part_2_answer

    @property
    def name(self):
        return f"Day {self._day:>2}"
