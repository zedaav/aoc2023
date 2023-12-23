import logging
from pathlib import Path
from typing import List, Set, Tuple

from aoc2023.puzzle import OFFSETS, AOCPuzzle, Direction

"""
Solutions for https://adventofcode.com/2023/day/23
"""

# Slopes to direction
SLOPES_TO_DIR = {"^": Direction.N, ">": Direction.E, "v": Direction.S, "<": Direction.W}


class D23Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.grid: List[str] = []
        self.width = None
        self.height = 0
        self.start = None
        super().__init__(input_file)
        self.end = (self.height - 1, self.grid[-1].find("."))
        logging.info(f"start: {self.start} / end: {self.end}")

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        self.grid.append(line)
        if self.width is None:
            self.width = len(line)
        self.height += 1

        if self.start is None:
            self.start = (0, line.find("."))

    def get_candidates(self, pos: Tuple[int, int], path: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
        # Direction may be forced by a slope
        row, col = pos
        if self.grid[row][col] in SLOPES_TO_DIR:
            dirs = [SLOPES_TO_DIR[self.grid[row][col]]]
        else:
            dirs = list(Direction)

        # Iterate on possible directions
        for col_offset, row_offset in map(OFFSETS.get, dirs):
            candidate_col, candidate_row = col + col_offset, row + row_offset
            candidate_pos = (candidate_row, candidate_col)
            if (
                candidate_pos not in path  # Not already done on this path
                and (0 <= candidate_col < self.width)  # Not out of col bounds
                and (0 <= candidate_row < self.height)  # Not out of row bounds
                and (self.grid[candidate_row][candidate_col] != "#")  # Not going in a tree
            ):
                yield candidate_pos

    def follow_paths(self, start: Tuple[int, int], path: Set[Tuple[int, int]] = None) -> List[Set[Tuple[int, int]]]:
        if path is None:
            path = {start}
        current = start
        while current != self.end:
            # Get candidate possible positions
            candidates = list(self.get_candidates(current, path))
            if len(candidates) == 1:
                # Follow path
                current = candidates[0]
                path.add(current)
            elif len(candidates) > 1:
                # Recurse into possible paths
                logging.info(f"Path split at {current} to {candidates}")
                out = []
                for candidate in candidates:
                    sub_path = set(path)
                    sub_path.add(candidate)
                    out.extend(self.follow_paths(candidate, sub_path))
                return out
            else:
                # No possible path from here... dead end?
                return []

        # Getting out of the loop: reached the end
        return [path]

    def solve(self) -> int:
        return max(len(p) for p in self.follow_paths(self.start)) - 1  # Don't count start position


class D23Step1Puzzle(D23Puzzle):
    # Default implementation
    pass


class D23Step2Puzzle(D23Puzzle):
    def solve(self) -> int:
        # Forget all special tiles
        new_grid = []
        for line in self.grid:
            new_line = line
            for k in SLOPES_TO_DIR.keys():
                new_line = new_line.replace(k, ".")
            new_grid.append(new_line)
        self.grid = new_grid

        return super().solve()
