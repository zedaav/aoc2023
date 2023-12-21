import logging
from pathlib import Path
from typing import Tuple

from aoc2023.puzzle import OFFSETS, AOCPuzzle, Direction

"""
Solutions for https://adventofcode.com/2023/day/21
"""


class D21Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.grid = []
        self.width = None
        self.height = 0
        self.start = None
        super().__init__(input_file)
        self.rock_set = {(r, c) for r in range(self.height) for c in range(self.width) if self.grid[r][c] == "#"}

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        self.grid.append(line)
        if self.width is None:
            self.width = len(line)
        self.height += 1

        if self.start is None:
            pos = line.find("S")
            if pos >= 0:
                self.start = (index - 1, pos)
                logging.info(f"Start found at row={self.start[0]}, col={self.start[1]}")

    def follow_step(self, pos: Tuple[int, int], steps_limit) -> int:
        # Keep track of add and even steps result
        even_positions = set()
        odd_positions = set()
        queue = [pos]
        steps = 0

        # Iterate until end condition
        while steps < steps_limit:
            steps += 1
            positions_set = odd_positions if steps % 2 else even_positions

            # Iterate on positions to be processed for this step
            new_queue = []
            while queue:
                row, col = queue.pop(0)

                # Iterate on directions
                for direction in Direction:
                    row_offset, col_offset = OFFSETS[direction]
                    new_row, new_col = row + row_offset, col + col_offset
                    new_pos = (new_row, new_col)
                    if (new_pos in self.rock_set) or (new_pos in positions_set):
                        # New position is either a rock, or already counted in this odd/even set
                        continue

                    # Remember as a new position to be processed
                    new_queue.append(new_pos)
                    positions_set.add(new_pos)
            queue = new_queue

        return len(even_positions)


class D21Step1Puzzle(D21Puzzle):
    def solve(self, steps: int) -> int:
        return self.follow_step(self.start, steps)


class D21Step2Puzzle(D21Puzzle):
    def solve(self) -> int:
        return 0
