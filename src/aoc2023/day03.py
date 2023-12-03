import re
from pathlib import Path

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/3
"""

# Numbers and symbols patterns
NUM_PATTERN = re.compile("([0-9]+)")
SMB_PATTERN = re.compile("[^0-9.]")
GEAR_PATTERN = re.compile(r"\*")


class D03Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        super().__init__(input_file)
        self.line_length = len(self.input_lines[0])

        # Prepend padded line in front of all lines
        self.padded_lines = ["." * self.line_length] + self.input_lines


class D03Step1Puzzle(D03Puzzle):
    def solve(self) -> int:
        # Iterate on lines to find numbers
        total_parts = 0
        for i in range(len(self.input_lines)):
            for m_num in re.finditer(NUM_PATTERN, self.input_lines[i]):
                # Number boundaries
                s, e = m_num.span()
                s, e = max(s - 1, 0), min(e + 1, self.line_length)

                # Build a single list with all symbols around the number
                symbols_around = "".join(r[s:e] for r in self.padded_lines[i : i + 3])
                if SMB_PATTERN.search(symbols_around):
                    # At least one symbol found around: this is a part number
                    total_parts += int(m_num.group(1))

        return total_parts


class D03Step2Puzzle(D03Puzzle):
    def solve(self) -> int:
        # Iterate on lines to find gears
        total_gears = 0
        for i in range(len(self.input_lines)):
            for m_gear in re.finditer(GEAR_PATTERN, self.input_lines[i]):
                # Find all numbers around
                numbers = []
                for r in self.padded_lines[i : i + 3]:
                    for m_nb in re.finditer(NUM_PATTERN, r):
                        if (m_nb.start() - 1) <= m_gear.start() <= m_nb.end():
                            numbers.append(int(m_nb.group(1)))
                if len(numbers) == 2:
                    total_gears += numbers[0] * numbers[1]

        return total_gears
