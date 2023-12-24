import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple

from aoc2023.puzzle import OFFSETS, AOCPuzzle, Direction

"""
Solutions for https://adventofcode.com/2023/day/23
"""

# Slopes to direction
SLOPES_TO_DIR = {"^": Direction.N, ">": Direction.E, "v": Direction.S, "<": Direction.W}


@dataclass
class Branch:
    a: Tuple[int, int]
    b: Tuple[int, int]
    path: Set[Tuple[int, int]]
    path_len: int


class D23Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.grid: List[str] = []
        self.width = None
        self.height = 0
        self.start = None
        super().__init__(input_file)
        self.end = (self.height - 1, self.grid[-1].find("."))
        logging.info(f"start: {self.start} / end: {self.end}")
        self.branches: Dict[Tuple[int, int], List[Branch]] = {}

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        self.grid.append(line)
        if self.width is None:
            self.width = len(line)
        self.height += 1

        if self.start is None:
            self.start = (0, line.find("."))

    def add_branch(self, a: Tuple[int, int], b: Tuple[int, int], path: Set[Tuple[int, int]], one_way: bool):
        if a not in self.branches:
            self.branches[a] = []
        b_path = set(path)
        b_path.discard(a)
        logging.info(f"New branch between {a} and {b} ({len(b_path)} steps)")
        self.branches[a].append(Branch(a, b, b_path, len(b_path)))
        if not one_way:
            if b not in self.branches:
                self.branches[b] = []
            b_path = set(path)
            b_path.discard(b)
            logging.info(f"New branch between {b} and {a} ({len(b_path)} steps)")
            self.branches[b].append(Branch(b, a, b_path, len(b_path)))

    def build_branches(self, start: Tuple[int, int], coming_from: Tuple[int, int] = None):
        branch_path = {start}
        branch_begin = start
        if coming_from is not None:
            branch_path.add(coming_from)
            branch_begin = coming_from
        current = start
        one_way = False
        while current != self.end:
            # Get candidate possible positions
            candidates = list(self.get_candidates(current, branch_path))
            if len(candidates) == 1:
                # Follow path
                current, change_one_way = candidates[0]
                one_way = one_way or change_one_way
                branch_path.add(current)
            elif len(candidates) > 1:
                # New branch done
                self.add_branch(branch_begin, current, branch_path, one_way)

                # Iterate on candidates to find new branches
                for candidate, _ in candidates:
                    if (current not in self.branches) or not any(candidate in b.path for b in self.branches[current]):
                        # Unknown branch from current node!
                        self.build_branches(candidate, current)
                return
            else:
                # No possible path from here... dead end?
                return

        # If getting here, remember the last branch
        self.add_branch(branch_begin, current, branch_path, one_way)

    def get_candidates(self, pos: Tuple[int, int], path: Set[Tuple[int, int]]) -> List[Tuple[Tuple[int, int], bool]]:
        # Direction may be forced by a slope
        row, col = pos
        if self.grid[row][col] in SLOPES_TO_DIR:
            dirs = [SLOPES_TO_DIR[self.grid[row][col]]]
            one_way = True
        else:
            dirs = list(Direction)
            one_way = False

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
                yield candidate_pos, one_way

    def follow_paths(self, start: Tuple[int, int], path: Dict[Tuple[int, int], int] = None) -> List[Dict[Tuple[int, int], int]]:
        if path is None:
            path = {start: 0}
        out = []

        # Must be a node
        assert start in self.branches

        # Iterate on possible branches (i.e. ones not already on path)
        for branch in filter(lambda br: br.b not in path, self.branches[start]):
            # Amend to path
            new_path = dict(path)
            new_path[branch.b] = branch.path_len
            if branch.b == self.end:
                # Final branch
                out.append(new_path)
            else:
                # Recurse into this new branch
                out.extend(self.follow_paths(branch.b, new_path))
        return out

    def solve(self) -> int:
        self.build_branches(self.start)
        return max(sum(p.values()) for p in self.follow_paths(self.start))


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
