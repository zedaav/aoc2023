import logging
import re
from pathlib import Path
from typing import List

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/14
"""

# Square rocks pattern
SQUARE_ROCKS = re.compile("[#]+")

# Round rocks pattern
ROUND_ROCKS = re.compile("[O]+")


# Model for parabolic reflector dish
class DishModel:
    def __init__(self, size: int, line: str = "") -> None:
        self.line = line
        self.size = size

    def add_line(self, line: str):
        self.line += line

    @property
    def lines(self) -> List[str]:
        return [self.line[self.size * i : self.size * (i + 1)] for i in range(len(self.line) // self.size)]

    def __repr__(self) -> str:
        return "\n".join(self.lines)

    def turn_right(self):  # -> DishModel
        # Build a new DishModel from current one, turned 90° on the right
        out = DishModel(self.size)
        for x in range(self.size):
            out.add_line("".join(row[x] for row in self.lines[::-1]))
        return out

    def tilt(self):  # -> DishModel
        # Build a new DishModel from current one, will all round rocks tilted on the right
        out = DishModel(self.size)
        for line in self.lines:
            # Iterate on square rocks groups
            new_line = ""
            previous_groups_end = 0
            for m_square in re.finditer(SQUARE_ROCKS, line):
                # Count all round rocks groups in the remaining space WRT. previous square rocks group
                total_nb = m_square.start() - previous_groups_end
                round_rocks_nb = sum(len(m) for m in re.findall(ROUND_ROCKS, line[previous_groups_end : m_square.start()]))

                # Append empty spaces + round rocks to new line
                new_line += "." * (total_nb - round_rocks_nb)
                new_line += "O" * round_rocks_nb

                # Add square rocks
                new_line += m_square.group(0)

                # Remember end for next iteration
                previous_groups_end = m_square.end()

            # Add line to new model
            out.add_line(new_line)
        return out

    def load(self) -> int:
        # Iterate on lines
        total_load = 0
        for line in self.lines:
            # Iterate on round rocks groups
            for m in re.finditer(ROUND_ROCKS, line):
                # Add load for all these rocks (load = rock position)
                total_load += sum(i for i in range(m.start(), m.end()))
        return total_load


class D14Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.initial_model: DishModel = None
        super().__init__(input_file)
        top_line = "#" * self.initial_model.size
        self.initial_model.line = top_line + self.initial_model.line + top_line

    def parse_line(self, index: int, line: str) -> str:
        # Parse lines, and surround initial pattern by square rocks
        line = "#" + super().parse_line(index, line) + "#"
        if self.initial_model is None:
            self.initial_model = DishModel(len(line))
        self.initial_model.add_line(line)


class D14Step1Puzzle(D14Puzzle):
    def solve(self) -> int:
        logging.info(f"initial model:\n{self.initial_model}")
        turned = self.initial_model.turn_right()
        logging.info(f"turned model:\n{turned}")
        tilted = turned.tilt()
        logging.info(f"tilted model:\n{tilted}")
        return tilted.load()


class D14Step2Puzzle(D14Puzzle):
    def cycle(self, model: DishModel) -> DishModel:
        # One complete cycle
        return model.turn_right().tilt().turn_right().tilt().turn_right().tilt().turn_right().tilt()

    def solve(self) -> int:
        model = self.initial_model

        # Cycle until we find a repeating pattern
        patterns = []
        next_pattern = model.line
        cycles_count = 0
        while next_pattern not in patterns:
            patterns.append(next_pattern)
            cycles_count += 1
            model = self.cycle(model)
            next_pattern = model.line
        logging.info(f"Found repeating pattern after {cycles_count} cycles")

        # Number of cycles until repeating pattern
        pattern_index = patterns.index(next_pattern)
        begin_cycles_nb = pattern_index

        # Number of cycles in repeating pattern
        pattern_cycles_nb = len(patterns) - pattern_index

        # Remaining number after the 1 Billion cycles
        remaining_cycles_nb = (1_000_000_000 - begin_cycles_nb) % pattern_cycles_nb
        logging.info(f"cycles: begin={begin_cycles_nb} pattern={pattern_cycles_nb} remaining={remaining_cycles_nb}")

        # Iterate again on remaining cycles number
        for _ in range(remaining_cycles_nb):
            model = self.cycle(model)

        # Turn a last time to get the load
        return model.turn_right().load()
