import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/5
"""

# Seeds single numbers
SEEDS_NUM = re.compile("([0-9]+)")

# Seeds pairs
SEEDS_PAIRS = re.compile("([0-9]+) +([0-9]+)")

# Map header
MAP_HEADER = re.compile("([a-z]+)-to-([a-z]+) map:")

# Map lines
MAP_LINE = re.compile("([0-9]+) +([0-9]+) +([0-9]+)")


@dataclass
class TypeMapper:
    source: str
    target: str
    types_map: Dict[Tuple[int, int], int]

    def process(self, ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        # Iterate on input digits
        out = []
        input_ranges = list(ranges)
        while len(input_ranges):
            # Iterate on known ranges
            x, y = input_ranges.pop()
            for (a, b), offset in self.types_map.items():
                if (a <= x <= b) and (a <= y <= b):
                    # Fully in range:
                    #    x.....y
                    #   a.........b
                    # Apply offset to both boundaries
                    out.append((x + offset, y + offset))
                    break
                if a <= x <= b:
                    # Overlapping:
                    #         x.....y
                    #   a.........b
                    # Split original range on upper boundary
                    out.append((x + offset, b + offset))
                    input_ranges.append((b + 1, y))
                    break
                if a <= y <= b:
                    # Overlapping:
                    #   x.....y
                    #      a.........b
                    # Split original range on lower boundary
                    out.append((a + offset, y + offset))
                    input_ranges.append((x, a - 1))
                    break
            else:
                # Out of any range:
                #   x.....y
                #             a......b
                # No process
                out.append((x, y))
        return out


class D05Puzzle(AOCPuzzle, ABC):
    def __init__(self, input_file: Path):
        self.seed_ranges = []
        self.mappers: Dict[str, TypeMapper] = {}
        self.next_mapper = None
        super().__init__(input_file)

        # Last line
        if self.next_mapper is not None:  # pragma: no branch
            self.mappers[self.next_mapper.source] = self.next_mapper
            logging.info(f"Found mapper: {self.next_mapper}")
            self.next_mapper = None

    @abstractmethod
    def parse_seeds(self, line):  # pragma: no cover
        pass

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)

        # Iterate on possible line types
        if line.startswith("seeds:"):
            # Seeds
            self.seed_ranges = self.parse_seeds(line)
            logging.info(f"Found seed ranges: {self.seed_ranges}")
        else:
            m = MAP_HEADER.match(line)
            if m is not None:
                # Map header
                self.next_mapper = TypeMapper(m.group(1), m.group(2), {})
            else:
                m = MAP_LINE.match(line)
                if m is not None:
                    # New map line
                    target_start, source_start, range_size = int(m.group(1)), int(m.group(2)), int(m.group(3))
                    self.next_mapper.types_map[(source_start, source_start + range_size - 1)] = target_start - source_start
                else:
                    # Empty line
                    if self.next_mapper is not None:
                        self.mappers[self.next_mapper.source] = self.next_mapper
                        logging.info(f"Found mapper: {self.next_mapper}")
                        self.next_mapper = None

    def solve(self) -> int:
        # Start from seeds, and iterate on mappers
        numbers = self.seed_ranges
        next_mapper_type = "seed"
        while next_mapper_type != "location":
            next_mapper = self.mappers[next_mapper_type]
            numbers = next_mapper.process(numbers)
            logging.info(f"{next_mapper.source} --> {next_mapper.target}: {numbers}")
            next_mapper_type = next_mapper.target
        return min(n[0] for n in numbers)


class D05Step1Puzzle(D05Puzzle):
    def parse_seeds(self, line):
        return [(int(m.group(1)), int(m.group(1))) for m in re.finditer(SEEDS_NUM, line)]


class D05Step2Puzzle(D05Puzzle):
    def parse_seeds(self, line):
        out = []
        for m in re.finditer(SEEDS_PAIRS, line):
            range_start, range_len = int(m.group(1)), int(m.group(2))
            out.append((range_start, range_start + range_len - 1))
        return out
