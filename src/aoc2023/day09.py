import logging
import re
from pathlib import Path

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/9
"""

# Number pattern
NUM_PATTERN = re.compile("([0-9-]+)")


class D09Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.seq_of_seqs = []
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Parse sequence
        line = super().parse_line(index, line)
        seq = [int(m.group(1)) for m in re.finditer(NUM_PATTERN, line)]
        logging.info(f"sequence at line {index}: {seq}")
        all_seqs = [seq]

        # Iterate until 0 delta, and build all derivated sequences
        go_on = True
        while go_on:
            in_work = all_seqs[-1]
            delta = [in_work[i + 1] - in_work[i] for i in range(0, len(in_work) - 1)]
            go_on = any(i != 0 for i in delta)
            all_seqs.append(delta)

        self.seq_of_seqs.append(all_seqs)


class D09Step1Puzzle(D09Puzzle):
    def solve(self) -> int:
        # Iterate on sequences
        total = 0
        for all_seqs in self.seq_of_seqs:
            # Predict next value
            for n in range(len(all_seqs) - 1, 0, -1):
                all_seqs[n - 1].append(all_seqs[n - 1][-1] + all_seqs[n][-1])

            # Sum
            total += all_seqs[0][-1]

        return total


class D09Step2Puzzle(D09Puzzle):
    def solve(self) -> int:
        # Iterate on sequences
        total = 0
        for all_seqs in self.seq_of_seqs:
            # Predict previous value
            for n in range(len(all_seqs) - 1, 0, -1):
                all_seqs[n - 1].insert(0, all_seqs[n - 1][0] - all_seqs[n][0])

            # Sum
            total += all_seqs[0][0]

        return total
