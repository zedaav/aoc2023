import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/6
"""


SEPARATED_DIGITS_PATTERN = re.compile("([0-9]+)")
ONE_BIG_DIGIT_PATTERN = re.compile("([0-9 ]+)")


@dataclass
class Record:
    time: int
    dist: int = 0


class D06Puzzle(AOCPuzzle, ABC):
    def __init__(self, input_file: Path):
        self.records: List[Record] = []
        super().__init__(input_file)
        logging.info(f"Parsed records: {self.records}")

    @abstractmethod
    def get_pattern(self) -> re.Pattern:  # pragma: no cover
        pass

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        if line.startswith("Time:"):
            for m in re.finditer(self.get_pattern(), line):
                self.records.append(Record(int(m.group(1).replace(" ", ""))))
        elif line.startswith("Distance:"):  # pragma: no branch
            for m, rec in zip(re.finditer(self.get_pattern(), line), self.records):
                rec.dist = int(m.group(1).replace(" ", ""))

    def solve(self) -> int:
        # t = time
        # d = distance record
        # x = hold time
        # we need to count number of x values (among 0..t range) for which (t-x)*x >= d
        # this is a parabolic function
        # --> just need to remove invalid values at the beginning of the range, *2 (same number of invalid values at the end of the range)

        # Iterate on records
        all_valid_values = 1
        for rec in self.records:
            # Eliminate invalid values
            valid_values = rec.time + 1
            x = 0
            while ((rec.time - x) * x) <= rec.dist:
                valid_values -= 2
                x += 1

            logging.info(f"For record {rec}: {valid_values} valid values")

            all_valid_values *= valid_values

        return all_valid_values


class D06Step1Puzzle(D06Puzzle):
    def get_pattern(self) -> re.Pattern:
        return SEPARATED_DIGITS_PATTERN


class D06Step2Puzzle(D06Puzzle):
    def get_pattern(self) -> re.Pattern:
        return ONE_BIG_DIGIT_PATTERN
