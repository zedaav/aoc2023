import logging
import re
from pathlib import Path
from typing import List, Tuple

from aoc2023.puzzle import OFFSETS, AOCPuzzle, Direction

"""
Solutions for https://adventofcode.com/2023/day/18
"""
# Instruction --> direction mapping
INSTR_2_DIR = {"U": Direction.N, "R": Direction.E, "L": Direction.W, "D": Direction.S}

# Instruction --> direction mapping
DIGIT_2_DIR = {"3": Direction.N, "0": Direction.E, "2": Direction.W, "1": Direction.S}

# Instructions pattern
INSTRUCTIONS = re.compile(f"([{''.join(INSTR_2_DIR.keys())}]) +([0-9]+) +\\(#([0-9a-f]+)\\)")


# See https://en.wikipedia.org/wiki/Shoelace_formula
def shoelace(points: List[Tuple[int, int]]):
    area = 0
    for (col1, row1), (col2, row2) in zip(points, points[1:] + [points[0]]):
        area += row1 * col2 - row2 * col1
    return area / 2


class D18Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.instructions: List[Tuple[Direction, int]] = []
        super().__init__(input_file)
        logging.info(f"Parsed instructions: {self.instructions}")

    def parse_line(self, index: int, line: str) -> str:
        m = INSTRUCTIONS.match(super().parse_line(index, line))
        if m is not None:  # pragma: no branch
            self.parse_instruction(m)

    def solve(self) -> int:
        # Start in 0,0
        col, row = (0, 0)
        points = [(col, row)]

        # Iterate on instructions
        for direction, distance in self.instructions:
            # Add blocks in grid
            col_offset, row_offset = OFFSETS[direction]
            col += col_offset * distance
            row += row_offset * distance
            points.append((col, row))
        logging.info(f"All points: {points}; shoelace: {shoelace(points)}")

        # See https://en.wikipedia.org/wiki/Pick%27s_theorem
        return int(-shoelace(points) + sum(distance for _, distance in self.instructions) / 2 + 1)


class D18Step1Puzzle(D18Puzzle):
    def parse_instruction(self, m: re.Match):
        self.instructions.append((INSTR_2_DIR[m.group(1)], int(m.group(2))))


class D18Step2Puzzle(D18Puzzle):
    def parse_instruction(self, m: re.Match):
        self.instructions.append((DIGIT_2_DIR[m.group(3)[-1]], int(m.group(3)[0:5], 16)))
