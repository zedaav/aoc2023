import logging
import re
from functools import cache
from pathlib import Path
from typing import Dict

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/15
"""


# Hash algorithm
@cache
def get_hash(input_str: str) -> int:
    out = 0
    for c in input_str:
        out += ord(c)
        out *= 17
        out %= 256
    return out


# Instruction pattern
INSTRUCTION = re.compile("([a-z]+)([-=])([0-9]+)?")


class D15Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.patterns = []
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        self.patterns.extend(super().parse_line(index, line).split(","))


class D15Step1Puzzle(D15Puzzle):
    def solve(self) -> int:
        return sum(map(get_hash, self.patterns))


class D15Step2Puzzle(D15Puzzle):
    def solve(self) -> int:
        # Follow instructions to fill the boxes
        boxes: Dict[int, Dict[str, int]] = {}
        for pattern in self.patterns:
            m = INSTRUCTION.match(pattern)
            assert m is not None

            # Identify box
            name = m.group(1)
            box_id = get_hash(name)
            if box_id not in boxes:
                boxes[box_id] = {}
            box = boxes[box_id]

            # Identify instruction
            if m.group(2) == "-":
                # Remove
                box.pop(name, None)
            else:
                # Add
                box[name] = int(m.group(3))
        logging.info("boxes:\n" + "\n".join(f"{k}: {v}" for k, v in boxes.items()))

        # Reckon focusing power
        power = 0
        for box_id, slots in boxes.items():
            for slot_id, focal in enumerate(slots.values(), 1):
                power += (box_id + 1) * slot_id * focal
        return power
