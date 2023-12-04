from pathlib import Path
import re
import logging
from dataclasses import dataclass
from typing import List, Dict

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/4
"""

# Pattern for line parsing
LINE_PATTERN = re.compile("Card +([0-9]+): ([^|]+)\\|(.+)")

# Pattern for numbers parsing
NUMBER_PATTERN = re.compile("[0-9]+")


@dataclass
class CardModel:
    index: int
    winning_ones: List[int]
    given_ones: List[int]

    @property
    def winning_numbers_count(self):
        return len(list(filter(lambda g: g in self.winning_ones, self.given_ones)))


class D04Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.cards: Dict[int, CardModel] = {}
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        m = LINE_PATTERN.match(super().parse_line(index, line))
        if m:  # pragma: no branch
            card = CardModel(
                int(m.group(1)),
                [int(n.group(0)) for n in re.finditer(NUMBER_PATTERN, m.group(2))],
                [int(n.group(0)) for n in re.finditer(NUMBER_PATTERN, m.group(3))],
            )
            self.cards[card.index] = card
            logging.info(f">>> card on line {index}: {card}")


class D04Step1Puzzle(D04Puzzle):
    def solve(self) -> int:
        # Iterate on cards
        score = 0
        for card in self.cards.values():
            if card.winning_numbers_count > 0:
                card_score = pow(2, card.winning_numbers_count - 1)
                logging.info(f"card {card.index} score: {card_score} ({card.winning_numbers_count})")
                score += card_score
        return score


class D04Step2Puzzle(D04Puzzle):
    def solve(self) -> int:
        # Prepare to count card instances
        instances_count = {i: 1 for i in range(1, len(self.cards) + 1)}

        # Iterate on cards
        for i in range(1, len(self.cards) + 1):
            # How many instances to add?
            new_instances = self.cards[i].winning_numbers_count
            for j in range(1, new_instances + 1):
                instances_count[i + j] += instances_count[i]
        return sum(instances_count.values())
