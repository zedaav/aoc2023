import logging
from enum import IntEnum, auto
from pathlib import Path

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/10
"""


class Direction(IntEnum):
    left = auto()
    right = auto()
    top = auto()
    bottom = auto()


OUTPUTS = {
    "-": {Direction.left: Direction.left, Direction.right: Direction.right},
    "|": {Direction.top: Direction.top, Direction.bottom: Direction.bottom},
    "7": {Direction.right: Direction.bottom, Direction.top: Direction.left},
    "L": {Direction.bottom: Direction.right, Direction.left: Direction.top},
    "J": {Direction.right: Direction.top, Direction.bottom: Direction.left},
    "F": {Direction.top: Direction.right, Direction.left: Direction.bottom},
}

NEXT = {Direction.left: (0, -1), Direction.right: (0, 1), Direction.top: (-1, 0), Direction.bottom: (1, 0)}


class D10Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.maze = []
        self.start = None
        super().__init__(input_file)
        self.size_x = len(self.maze[0])
        self.size_y = len(self.maze)
        self.paths_nodes = []

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        if "S" in line:
            self.start = (index - 1, line.find("S"))
            logging.info(f"Start found at {self.start}")
        self.maze.append(line)

    def solve(self) -> int:
        # Find paths from start
        s_y, s_x = self.start
        paths_current = []
        directions = []
        for d in Direction:
            c_y, c_x = (s_y + NEXT[d][0], s_x + NEXT[d][1])
            if not ((0 <= c_y <= self.size_y) and (0 <= c_x <= self.size_x)):
                continue
            c_step = self.maze[c_y][c_x]
            if c_step in OUTPUTS and d in OUTPUTS[c_step]:
                paths_current.append((c_y, c_x))
                s = set()
                s.add((c_y, c_x))
                self.paths_nodes.append(s)
                directions.append(d)

        logging.info(f"Path starts: {paths_current}")
        assert len(paths_current) == 2
        steps = 1
        go_on = True
        while go_on:
            for i in range(len(paths_current)):
                # Move next
                s_y, s_x = paths_current[i]
                s_step = self.maze[s_y][s_x]
                d = OUTPUTS[s_step][directions[i]]
                c_y, c_x = (s_y + NEXT[d][0], s_x + NEXT[d][1])
                self.paths_nodes[i].add((c_y, c_x))
                paths_current[i] = (c_y, c_x)
                directions[i] = d

                # Continue only if not already in the other path
                go_on = (c_y, c_x) not in self.paths_nodes[(i + 1) % 2]
            steps += 1
        return steps


class D10Step1Puzzle(D10Puzzle):
    pass


class D10Step2Puzzle(D10Puzzle):
    def solve(self) -> int:
        # Find all maze nodes
        super().solve()
        all_nodes = self.paths_nodes[0].union(self.paths_nodes[1])
        all_nodes.add((self.start))

        # Iterate on all nodes
        all_inside = 0
        for y in range(self.size_y):
            in_loop = 0
            for x in range(self.size_x):
                if (y, x) in all_nodes:
                    # Vertical pipe?
                    if self.maze[y][x] in "|JL":
                        in_loop = (in_loop + 1) % 2
                else:
                    # Count cell if in the loop
                    all_inside += in_loop

        return all_inside
