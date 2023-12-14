import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/13
"""


@dataclass
class Pattern:
    coef: int
    patterns: List[str]
    mirrors: List[int]


def find_smudge(a: str, b: str) -> int:
    diff = None
    for index, (c_a, c_b) in enumerate(zip(a, b)):
        if c_a != c_b:
            if diff is not None:
                # There already a diff: give up
                return None
            diff = index
    return diff


class D13Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.candidate = None
        self.patterns = []
        super().__init__(input_file)
        self.end_pattern()

    def add_pattern(self, line: str, candidate: Pattern):
        candidate.patterns.append(line)
        if len(candidate.patterns) > 1 and candidate.patterns[-1] == candidate.patterns[-2]:
            candidate.mirrors.append(len(candidate.patterns) - 1)

    def end_pattern(self):
        if self.candidate is None:  # pragma: no cover
            return

        # Build another pattern with reversed lines
        reversed_pattern = Pattern(1, [], [])
        for x in range(len(self.candidate.patterns[0])):
            line = "".join(row[x] for row in self.candidate.patterns)
            self.add_pattern(line, reversed_pattern)

        # Add pair of patterns
        self.patterns.append((self.candidate, reversed_pattern))
        logging.info(f"new pattern: {self.patterns[-1]}")

        # No more candidate
        self.candidate = None

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        if line:
            if self.candidate is None:
                self.candidate = Pattern(100, [], [])
            self.add_pattern(line, self.candidate)
        else:
            self.end_pattern()

    def validate_mirror(self, pattern: Pattern) -> int:
        # Find real reflexions
        mirrors = pattern.mirrors
        mirror = None
        mirror_found = False
        while len(mirrors) > 0 and not mirror_found:
            # Loop while more than one mirror line
            mirror = mirrors.pop()

            # Compare lines
            mirror_found = True
            for i in range(min(mirror, len(pattern.patterns) - mirror)):
                if pattern.patterns[mirror + i] != pattern.patterns[mirror - i - 1]:
                    mirror_found = False
                    break

        if mirror_found:
            logging.info(f"mirror found: {mirror} * {pattern.coef}")
            return pattern.coef * mirror
        return 0


class D13Step1Puzzle(D13Puzzle):
    def solve(self) -> int:
        # Iterate on patterns
        total = 0
        for patterns_pair in self.patterns:
            # Iterate on pairs
            for pattern in patterns_pair:  # pragma: no branch
                # Find real reflexions
                res = self.validate_mirror(pattern)
                if res != 0:
                    # Break on patterns pair (no need to analyze other pattern)
                    total += res
                    break

        return total


class D13Step2Puzzle(D13Puzzle):
    def solve(self) -> int:
        # Find potential smudges: iterate on patterns
        total = 0
        for pattern_id, patterns_pair in enumerate(self.patterns):
            # Iterate on pairs
            pattern_found = False
            for pair_id, pattern in enumerate(patterns_pair):  # pragma: no branch
                # Iterate on lines to find smudges
                for index, line in enumerate(pattern.patterns):
                    for offset in range(1, len(pattern.patterns) - index, 2):
                        smudge_candidate = find_smudge(line, pattern.patterns[index + offset])
                        if smudge_candidate is not None:
                            mirror = index + (offset // 2) + 1
                            logging.info(
                                f"pattern {pattern_id}, pair {pair_id}: smudge candidate: {index}<-->{index+offset} (mirror {mirror}), character {smudge_candidate}"
                            )

                            # Test with this smudge candidate
                            new_pattern = Pattern(pattern.coef, list(pattern.patterns), [mirror])
                            new_pattern.patterns[index] = new_pattern.patterns[index + offset]
                            res = self.validate_mirror(new_pattern)
                            if res > 0:
                                total += res
                                pattern_found = True
                                break
                    if pattern_found:
                        break
                if pattern_found:
                    break

        return total
