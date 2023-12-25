import logging
import re
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import List, Tuple

import numpy as np
from z3 import IntVector, Solver

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/24
"""

# Hailstone pattern
HAILSTONE = re.compile("([-0-9]+), +([-0-9]+), +([-0-9]+) +@ +([-0-9]+), +([-0-9]+), +([-0-9]+)")


# Sign
def sign_of(a: int) -> int:
    if a == 0:
        return 0
    return a // abs(a)


# Hailstone model
@dataclass
class HailStone:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

    def dist_2d(self, other: object) -> int:
        # 2D distance between 2 hailstones
        return abs(self.delta_x(other)) + abs(self.delta_y(other))

    def delta_x(self, other: object) -> int:
        return self.px - other.px

    def delta_y(self, other: object) -> int:
        return self.py - other.py

    def move(self, t: int) -> object:
        # Returns a copy of this hailstone in the future, with its new position
        return HailStone(self.px + self.vx * t, self.py + self.vy * t, self.pz + self.vz * t, self.vx, self.vy, self.vz)

    def time_for_x(self, x: int) -> float:
        # Get time at which x will reach required position
        return (x - self.px) / self.vx

    def time_for_y(self, y: int) -> float:
        # Get time at which y will reach required position
        return (y - self.py) / self.vy

    def boundary_time(self, pos: int, check) -> float:
        t1, t2 = self.time_for_x(pos), self.time_for_y(pos)
        pos = self.move(t1)
        if check(pos.px) and check(pos.py):
            return t1
        pos = self.move(t2)
        if check(pos.px) and check(pos.py):
            return t2

        raise AssertionError("Can't find boundary time")

    def boundary_times(self, boundaries: Tuple[int, int]) -> Tuple[float, float]:
        # Get times when this instance enters and leaves the test area boundaries
        pos_min, pos_max = boundaries
        t_min = self.boundary_time(pos_min, lambda pos: pos >= pos_min)
        t_max = self.boundary_time(pos_max, lambda pos: pos <= pos_max)
        return (min(t_min, t_max), max(t_min, t_max))


class D24Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.hailstones: List[HailStone] = []
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        m = HAILSTONE.match(line)
        assert m is not None
        self.hailstones.append(HailStone(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6))))
        logging.info(f"Parsed hailstone: {self.hailstones[-1]}")


class D24Step1Puzzle(D24Puzzle):
    def solve(self, boundaries: Tuple[int, int]) -> int:
        # Iterate on all combinations
        total = 0
        b_min, b_max = boundaries
        for hs1, hs2 in combinations(self.hailstones, 2):
            # Get slopes
            s1 = hs1.vy / hs1.vx
            s2 = hs2.vy / hs2.vx

            # Filter out parallel paths
            if s1 == s2:
                # Same slope means parallel paths, skip this pair
                continue

            # Find x and y to get both:
            # -s1 * x + y = -s1 * hs1.px + hs1.py
            # -s2 * x + y = -s2 * hs2.px + hs2.py
            x, y = np.linalg.solve([[-s1, 1], [-s2, 1]], [-s1 * hs1.px + hs1.py, -s2 * hs2.px + hs2.py])

            # Filter if found intersection is in the past
            if (((x - hs1.px) / hs1.vx) < 0) or (((x - hs2.px) / hs2.vx) < 0):
                continue

            # Only count intersections within test area
            if (b_min <= x <= b_max) and (b_min <= y <= b_max):
                total += 1

        return total


class D24Step2Puzzle(D24Puzzle):
    def solve(self) -> int:
        # Prepare int vector for solution
        px, py, pz, vx, vy, vz = IntVector("solution", 6)
        times = IntVector("time", len(self.hailstones))
        s = Solver()

        # Add all constraints
        for t, hs in zip(times, self.hailstones):
            s.add(px + t * vx == hs.px + t * hs.vx)
            s.add(py + t * vy == hs.py + t * hs.vy)
            s.add(pz + t * vz == hs.pz + t * hs.vz)

        # Solve this
        s.check()
        m = s.model()

        return m[px].as_long() + m[py].as_long() + m[pz].as_long()
