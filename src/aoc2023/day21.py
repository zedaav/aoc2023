import logging
from collections import defaultdict
from pathlib import Path

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

    def possible_points(self, point):
        # Loop over all possible directions, and yield each possible new point
        # Check the remainder of the point axis' divided by grid size to continue moving outward infinitely for part 2
        for d in Direction:
            offset = OFFSETS[d]
            new_point = (point[0] + offset[0], point[1] + offset[1])
            if self.grid[new_point[1] % self.height][new_point[0] % self.width] != "#":  # Make sure it wasn't a rock
                yield new_point

    def bfs(self, point, max_dist):
        # Use the Breadth first search to find the number of points hit each step, and return the dictionary with key of number of steps taken,
        # and value of number of points hit
        tiles = defaultdict(int)
        visited = set()
        queue = [(point, 0)]
        while queue:  # End when the queue is empty
            curr_point, dist = queue.pop(0)
            if dist == (max_dist + 1) or curr_point in visited:  # Don't include points that have already been visited
                continue

            tiles[dist] += 1
            visited.add(curr_point)

            for next_point in self.possible_points(curr_point):  # Loop over possible points and add to queue
                queue.append((next_point, (dist + 1)))
        return tiles

    def calculate_possible_spots(self, start, max_steps):
        # Get the output from bfs, and then return the sum of all potential stopping points in the tiles output based on even numbers
        tiles = self.bfs(start, max_steps)
        return sum(amount for distance, amount in tiles.items() if distance % 2 == max_steps % 2)

    def quad(self, y, n):
        # Use the quadratic formula to find the output at the large steps based on the first three data points
        a = (y[2] - (2 * y[1]) + y[0]) // 2
        b = y[1] - y[0] - a
        c = y[0]
        return (a * n**2) + (b * n) + c


class D21Step1Puzzle(D21Puzzle):
    def solve(self, steps: int) -> int:
        return self.calculate_possible_spots(self.start, steps)


class D21Step2Puzzle(D21Puzzle):
    def solve(self, steps: int) -> int:
        # Calculate the first three data points for use in the quadratic formula, and then return the output of quad
        size = self.height
        edge = size // 2

        y = [self.calculate_possible_spots(self.start, (edge + i * size)) for i in range(3)]

        return self.quad(y, ((steps - edge) // size))

    def solve2(self, steps: int) -> int:
        # Possible spots in 3 positions
        half = self.width // 2
        candidates = [self.follow_steps(half + i * self.width) for i in range(3)]

        # Quadratic formula
        a = (candidates[2] - (2 * candidates[1]) + candidates[0]) // 2
        b = candidates[1] - candidates[0] - a
        c = candidates[0]
        n = (steps - half) // self.width
        return (a * n**2) + (b * n) + c
