import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/22
"""

# Brick positions
BRICK_PATTERN = re.compile("([0-9]+),([0-9]+),([0-9]+)~([0-9]+),([0-9]+),([0-9]+)")


# Brick model
@dataclass
class Brick:
    nb: int
    top: int
    bottom: int
    plan_cubes: Set[Tuple[int, int]]
    bricks_above: Set[int] = field(default_factory=set)
    bricks_below: Set[int] = field(default_factory=set)


class D22Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.highest_bottom = 1
        self.bricks: Dict[int, Brick] = {}
        self.min_x = self.min_y = self.max_x = self.max_y = None
        self.next_brick_nb = 1
        super().__init__(input_file)
        logging.info(f"plan corners: {self.min_x},{self.min_y} - {self.max_x},{self.max_y}")
        logging.info(f"highest brick bottom: {self.highest_bottom}")

        # Simplify: both x and y are supposed to be 0-based
        assert self.min_x == 0
        assert self.min_y == 0

        # Base skyline: bricks already lying on the ground
        self.skyline: List[List[Brick]] = []
        for _ in range(self.max_x + 1):
            line = []
            self.skyline.append(line)
            for _ in range(self.max_y + 1):
                line.append(None)

    def parse_line(self, index: int, line: str) -> str:
        # Parse brick
        line = super().parse_line(index, line)
        m = BRICK_PATTERN.match(line)
        assert m is not None
        x1, y1, z1, x2, y2, z2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6))
        plan_cubes = set()
        min_x, min_y, max_x, max_y = min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                plan_cubes.add((x, y))
        brick = Brick(self.next_brick_nb, max(z1, z2), min(z1, z2), plan_cubes)
        self.next_brick_nb += 1
        logging.info(f"new brick: {brick}")

        # Upgrade highest bottom
        if brick.bottom > self.highest_bottom:
            self.highest_bottom = brick.bottom

        # Upgrade plan corners
        if self.min_x is None or min_x < self.min_x:
            self.min_x = min_x
        if self.max_x is None or max_x > self.max_x:
            self.max_x = max_x
        if self.min_y is None or min_y < self.min_y:
            self.min_y = min_y
        if self.max_y is None or max_y > self.max_y:
            self.max_y = max_y

        # Add to bricks list
        self.bricks[brick.nb] = brick


class D22Step1Puzzle(D22Puzzle):
    def solve(self) -> int:
        # Step 1: let all bricks fall

        # Iterate on all bricks (sorted by bottom)
        for brick in sorted(self.bricks.values(), key=lambda b: b.bottom):
            # Reckon gap between this brick and the skyline below
            former_sky_limit = max(self.skyline[x][y].top if self.skyline[x][y] is not None else 0 for x, y in brick.plan_cubes)
            gap = brick.bottom - 1 - former_sky_limit
            if gap:
                # Decrease z (bottom/top) by this gap
                brick.bottom -= gap
                brick.top -= gap

            # Iterate of cubes covered by this brick
            for x, y in brick.plan_cubes:
                # Remember the brick just below, if any
                below_candidate = self.skyline[x][y]
                if (below_candidate is not None) and (below_candidate.top == brick.bottom - 1):
                    brick.bricks_below.add(below_candidate.nb)
                    below_candidate.bricks_above.add(brick.nb)

                # Update skyline with this brick
                self.skyline[x][y] = brick

        logging.info("after fall:\n" + "\n".join(str(b) for b in self.bricks.values()))

        # Step 2: count all bricks that can be desintegrated
        total = 0
        for brick in self.bricks.values():
            count_it = True
            for above_one in map(self.bricks.get, brick.bricks_above):
                if len(above_one.bricks_below) == 1:
                    # Current brick is the only one supporting this one, give up
                    assert brick.nb in above_one.bricks_below
                    count_it = False
                    break
            if count_it:
                total += 1

        return total


class D22Step2Puzzle(D22Puzzle):
    def solve(self) -> int:
        return 0
