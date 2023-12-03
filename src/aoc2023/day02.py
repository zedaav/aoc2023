import logging
import re
from pathlib import Path

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/2
"""


# Game line pattern
GAME_PATTERN = re.compile("Game ([0-9]+): (.+)")

# Red/Green/Blue cube patterns
RED_PATTERN = re.compile("([0-9]+) red")
GREEN_PATTERN = re.compile("([0-9]+) green")
BLUE_PATTERN = re.compile("([0-9]+) blue")


class D02Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.games = {}
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call to get line
        m = GAME_PATTERN.match(super().parse_line(index, line))
        if m is not None:  # pragma: no branch
            g_id = int(m.group(1))
            g_sets = []
            for g_set in m.group(2).split("; "):
                r = g = b = 0
                for c_str in g_set.split(", "):
                    m = RED_PATTERN.match(c_str)
                    if m is not None:
                        r = int(m.group(1))
                    m = GREEN_PATTERN.match(c_str)
                    if m is not None:
                        g = int(m.group(1))
                    m = BLUE_PATTERN.match(c_str)
                    if m is not None:
                        b = int(m.group(1))
                g_sets.append((r, g, b))
            self.games[g_id] = g_sets
            logging.info(f">>> game {g_id}: {g_sets}")


class D02Step1Puzzle(D02Puzzle):
    def solve(self) -> int:
        possible_games = []
        for g_id, g_sets in self.games.items():
            ok_to_add = True
            for r, g, b in g_sets:
                if (r > 12) or (g > 13) or (b > 14):
                    ok_to_add = False
                    break
            if ok_to_add:
                possible_games.append(g_id)
        return sum(possible_games)


class D02Step2Puzzle(D02Puzzle):
    def solve(self) -> int:
        powers = []
        for g_sets in self.games.values():
            max_r = max_g = max_b = 0
            for r, g, b in g_sets:
                max_r = max(r, max_r)
                max_g = max(g, max_g)
                max_b = max(b, max_b)
            powers.append(max_r * max_g * max_b)
        return sum(powers)
