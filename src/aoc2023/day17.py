import heapq
from pathlib import Path
from typing import List, Tuple, Union

from aoc2023.puzzle import OFFSETS, OPPOSITE, AOCPuzzle, Direction

"""
Solutions for https://adventofcode.com/2023/day/17
"""


class D17Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.grid = []
        self.width = None
        self.height = 0
        super().__init__(input_file)
        self.start = (0, 0)
        self.end = (self.width - 1, self.height - 1)

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        self.grid.append([int(c) for c in line])
        if self.width is None:
            self.width = len(line)
        self.height += 1

    def get_candidates_directions(self, direction: Direction) -> List[Direction]:
        # Iterate an all directions except the opposite of the incoming one (don't get back)
        for d in filter(lambda d: (direction is None) or (d not in [direction, OPPOSITE[direction]]), Direction):
            yield d

    def next_pos(self, point: Tuple[int, int], direction: Direction, distance: int) -> Union[Tuple[int, int], None]:
        # Move in required direction, on the required distance
        o = OFFSETS[direction]
        p = (point[0] + o[0] * distance, point[1] + o[1] * distance)
        if (0 <= p[0] < self.width) and (0 <= p[1] < self.height):
            # Not out of grid
            return p

    def best_path(self, min_dist: int, max_dist: int) -> int:
        q = [(0, self.start, None)]
        best_paths = {}
        while q:  # pragma: no branch
            # Get best cost
            cost, point, direction = heapq.heappop(q)

            # End of the way?
            if point == self.end:
                return cost

            # Iterate on candidate directions
            for c_direction in self.get_candidates_directions(direction):
                cost_offset = 0
                # Iterate on moving forward in the same direction
                for distance in range(1, max_dist + 1):
                    # Check if next point is still in grid
                    c_point = self.next_pos(point, c_direction, distance)
                    if c_point:
                        # New cost for this position
                        col, row = c_point
                        cost_offset += self.grid[row][col]

                        # Can't turn before min distance is ran
                        if distance < min_dist:
                            continue

                        new_cost = cost + cost_offset
                        if (c_point, c_direction) not in best_paths or (new_cost < best_paths[(c_point, c_direction)]):
                            # Ok, new "best path" candidate
                            best_paths[(c_point, c_direction)] = new_cost
                            heapq.heappush(q, (new_cost, c_point, c_direction))
                    else:
                        # No need to loop anymore in this direction: out of grid
                        break


class D17Step1Puzzle(D17Puzzle):
    def solve(self) -> int:
        return self.best_path(1, 3)


class D17Step2Puzzle(D17Puzzle):
    def solve(self) -> int:
        return self.best_path(4, 10)
