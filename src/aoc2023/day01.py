import logging
from pathlib import Path

from aoc2023.puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2023/day/1
"""


class D01Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.digits = []
        super().__init__(input_file)

    def solve(self) -> int:
        # Loop on digits and sum first*10 + last
        return sum(10 * digits[0] + digits[-1] for digits in self.digits)


class D01Step1Puzzle(D01Puzzle):
    def parse_line(self, index: int, line: str) -> str:
        # Parse digits
        line_digits = [int(i) for i in filter(lambda c: c >= "0" and c <= "9", super().parse_line(index, line))]
        self.digits.append(line_digits)
        logging.info(f"digits for line {index}: {line_digits[0]} and {line_digits[-1]}")


# Map for digits mapping
DIGITS_MAP = {
    "0": 0,
    "zero": 0,
    "1": 1,
    "one": 1,
    "2": 2,
    "two": 2,
    "3": 3,
    "three": 3,
    "4": 4,
    "four": 4,
    "5": 5,
    "five": 5,
    "6": 6,
    "six": 6,
    "7": 7,
    "seven": 7,
    "8": 8,
    "eight": 8,
    "9": 9,
    "nine": 9,
}


class D01Step2Puzzle(D01Puzzle):
    def parse_line(self, index: int, line: str) -> str:
        # Look for digit strings in line
        line = super().parse_line(index, line)
        line_digits = []
        line_length = len(line)
        i = 0
        while i < line_length:
            for d_n, d_v in filter(lambda t: len(t[0]) <= (line_length - i), DIGITS_MAP.items()):
                if line[i : i + len(d_n)] == d_n:
                    line_digits.append(d_v)
            # Just increment by one, since there may be overlaps like "twone" or "nineight"
            i += 1
        self.digits.append(line_digits)
        logging.info(f"digits for line {index}: {line_digits[0]} and {line_digits[-1]}")
