import logging
import re
from functools import cache
from pathlib import Path
from typing import Tuple

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/12
"""

# Line pattern
LINE_PATTERN = re.compile("([.#?]+) +([0-9,]+)")


# Count possible solutions (with cache to improve performances on repeated patterns)
@cache
def count_solutions(search_space: str, sizes: Tuple[int], done: int = 0) -> int:
    # Nothing more in string?
    if len(search_space) == 0:
        # Solution found if no more sizes to resolve
        return 1 if ((len(sizes) == 0) and (done == 0)) else 0

    # Number of solutions
    nb = 0

    # Possible branches
    branches = [".", "#"] if (search_space[0] == "?") else search_space[0]
    for c in branches:
        # New damaged spring?
        if c == "#":
            # Yes: recursive call on next step
            nb += count_solutions(search_space[1:], sizes, done + 1)
        else:
            # No: running group?
            if done:
                # Yes: group is resolved?
                if (len(sizes) > 0) and (sizes[0] == done):
                    # Go to next group
                    nb += count_solutions(search_space[1:], sizes[1:])
            else:
                # Was not is a running group, simply go forward
                nb += count_solutions(search_space[1:], sizes)

    return nb


class D12Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.lines = []
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        m = LINE_PATTERN.match(super().parse_line(index, line))
        if m:  # pragma: no branch
            search_space = m.group(1)
            sizes = tuple(int(g) for g in m.group(2).split(","))
            logging.info(f"New line: {search_space} {sizes}")
            self.lines.append((search_space, sizes))


class D12Step1Puzzle(D12Puzzle):
    def solve(self) -> int:
        # Iterate on lines
        total = 0
        for search_space, sizes in self.lines:
            total += count_solutions(search_space + ".", sizes)

        return total


class D12Step2Puzzle(D12Puzzle):
    def solve(self) -> int:
        # Iterate on lines
        total = 0
        for search_space, sizes in self.lines:
            total += count_solutions("?".join([search_space] * 5) + ".", sizes * 5)

        return total
