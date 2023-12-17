from pathlib import Path
from typing import Dict, Set, Tuple

from aoc2023.puzzle import OFFSETS, AOCPuzzle, Direction

"""
Solutions for https://adventofcode.com/2023/day/16
"""


# Turn instructions
TURN_TO = {
    "/": {
        Direction.N: Direction.E,
        Direction.E: Direction.N,
        Direction.S: Direction.W,
        Direction.W: Direction.S,
    },
    "\\": {
        Direction.N: Direction.W,
        Direction.E: Direction.S,
        Direction.S: Direction.E,
        Direction.W: Direction.N,
    },
}


# Split instructions
SPLIT_TO = {"-": (Direction.E, Direction.W), "|": (Direction.N, Direction.S)}


class D16Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.contraption = ""
        self.size_x = None
        self.size_y = 0
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        self.contraption += line
        self.size_y += 1
        if self.size_x is None:
            self.size_x = len(line)

    # Energized tiles count reckon function
    def follow(self, pos: Tuple[int, int], direction: Direction, visited: Dict[Tuple[int, int], Set[Direction]]) -> int:
        # Follow position until getting out of the box
        while (0 <= pos[0] < self.size_x) and (0 <= pos[1] < self.size_y) and (direction not in visited.get(pos, set())):
            # Position is now energized
            directions = visited.setdefault(pos, set())
            directions.add(direction)

            # Check tile on position
            tile = self.contraption[pos[1] * self.size_x + pos[0]]
            if (tile == ".") or (tile in SPLIT_TO and direction in SPLIT_TO[tile]):
                # Ok, go forward
                pass
            elif tile in ["/", "\\"]:
                # Turn, and go forward
                direction = TURN_TO[tile][direction]
            else:
                # Split
                self.follow(pos, SPLIT_TO[tile][0], visited)
                direction = SPLIT_TO[tile][1]

            # Move
            m = OFFSETS[direction]
            pos = (pos[0] + m[0], pos[1] + m[1])
        return len(visited)


class D16Step1Puzzle(D16Puzzle):
    def solve(self) -> int:
        return self.follow((0, 0), Direction.E, {})


class D16Step2Puzzle(D16Puzzle):
    def solve(self) -> int:
        # Maximize energized tiles for all starting positions
        energized = []
        for x in range(self.size_x):
            for y, direction in zip((0, self.size_y - 1), (Direction.S, Direction.N)):
                energized.append(self.follow((x, y), direction, {}))
        for y in range(self.size_y):
            for x, direction in zip((0, self.size_x - 1), (Direction.E, Direction.W)):
                energized.append(self.follow((x, y), direction, {}))
        return max(energized)
