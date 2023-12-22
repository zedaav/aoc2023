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
    saved_top: int = None
    saved_bottom: int = None

    def reset(self):
        self.top = self.saved_top
        self.bottom = self.saved_bottom

    def save(self):
        self.saved_top = self.top
        self.saved_bottom = self.bottom


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

    def fall(self, bricks_to_fall: List[Brick], init_related: bool = False) -> List[Brick]:
        # Prepare skyline
        skyline: List[List[Brick]] = []
        for _ in range(self.max_x + 1):
            line = []
            skyline.append(line)
            for _ in range(self.max_y + 1):
                line.append(None)

        # Fall from initial state; iterate on all bricks (sorted by bottom)
        falling_bricks = []
        for brick in bricks_to_fall:
            # Save top+bottom if this is the first fall
            if init_related:
                brick.save()

            # Reckon gap between this brick and the skyline below
            former_sky_limit = max(skyline[x][y].top if skyline[x][y] is not None else 0 for x, y in brick.plan_cubes)
            gap = brick.bottom - 1 - former_sky_limit
            if gap > 0:
                # Decrease z (bottom/top) by this gap
                brick.bottom -= gap
                brick.top -= gap
                falling_bricks.append(brick)

                # Save top+bottom if this is the first fall
                if init_related:
                    brick.save()

            # Iterate of cubes covered by this brick
            for x, y in brick.plan_cubes:
                # Remember the brick just below, if any
                if init_related:
                    below_candidate = skyline[x][y]
                    if (below_candidate is not None) and (below_candidate.top == brick.bottom - 1):
                        brick.bricks_below.add(below_candidate.nb)
                        below_candidate.bricks_above.add(brick.nb)

                # Update skyline with this brick
                skyline[x][y] = brick
        return falling_bricks

    def fall_and_count(self, count_safe: bool = True) -> List[Brick]:
        # Make them fall
        self.fall(sorted(self.bricks.values(), key=lambda b: b.bottom), init_related=True)

        # List all bricks that, when desintegrated:
        # * if count_safe = True: don't make any other bricks falling
        # * if count_safe = False: make any other bricks falling
        out = []
        for brick in self.bricks.values():
            count_it = count_safe
            for above_one in map(self.bricks.get, brick.bricks_above):
                if len(above_one.bricks_below) == 1:
                    # Current brick is the only one supporting this one
                    assert brick.nb in above_one.bricks_below
                    count_it = not count_safe
                    break
            if count_it:
                out.append(brick)

        return out


class D22Step1Puzzle(D22Puzzle):
    def solve(self) -> int:
        # Count all bricks that can be desintegrated
        return len(self.fall_and_count())


class D22Step2Puzzle(D22Puzzle):
    def solve(self) -> int:
        # Iterate on all bricks that make above ones falling if desintegrated
        desintegrated_ones = sorted(self.fall_and_count(count_safe=False), key=lambda b: b.bottom)
        original_ones = sorted(self.bricks.values(), key=lambda b: b.bottom)
        total = 0
        for desintegrated in desintegrated_ones:
            # Make bricks fall again, without disintegrated one
            falling_bricks = self.fall(filter(lambda b: b != desintegrated, original_ones))
            total += len(falling_bricks)

            # Reset falling bricks to their original position
            for b in falling_bricks:
                b.reset()

        return total
