import logging
from pathlib import Path
import re
from itertools import combinations

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/11
"""


class D11Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.galaxies = []
        self.empty_rows = []
        self.empty_cols = []
        self.universe = []
        super().__init__(input_file)
        self.size_cols = len(self.universe[0])
        self.size_rows = len(self.universe)

        # Find also empty columns
        for x in range(self.size_cols):
            if not any(self.universe[y][x] == "#" for y in range(self.size_rows)):
                self.empty_cols.append(x)

        logging.info(f"Empty rows: {self.empty_rows}")
        logging.info(f"Empty columns: {self.empty_cols}")
        logging.info(f"Galaxies: {len(self.galaxies)}")

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        self.universe.append(line)
        galaxy_found = False
        for m in re.finditer("#", line):
            # One more galaxy
            self.galaxies.append((index - 1, m.start()))
            galaxy_found = True

        if not galaxy_found:
            # No galaxy on the row: empty line
            self.empty_rows.append(index - 1)

    def solve(self, age_factor: int) -> int:
        # Iterate on pairs
        total = 0
        for (y1, x1), (y2, x2) in combinations(self.galaxies, 2):
            # Basic path length
            min_x = min(x1, x2)
            min_y = min(y1, y2)
            max_x = max(x1, x2)
            max_y = max(y1, y2)
            path = (max_y - min_y) + (max_x - min_x)

            # Add expanded rows/cols if any
            for _ in filter(lambda c: min_x < c < max_x, self.empty_cols):
                path += age_factor - 1
            for _ in filter(lambda c: min_y < c < max_y, self.empty_rows):
                path += age_factor - 1

            total += path
        return total
