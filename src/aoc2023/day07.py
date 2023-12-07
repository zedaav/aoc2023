from typing import Dict
from abc import ABC, abstractmethod
import logging
import re
from dataclasses import dataclass
from pathlib import Path

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/7
"""

# Hand pattern
HAND_PATTERN = re.compile("([0-9TJQKA]+) +([0-9]+)")

# Map for comparison string
STEP1_COMP_CHAR = {
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "T": "A",
    "J": "B",
    "Q": "C",
    "K": "D",
    "A": "E",
}
STEP2_COMP_CHAR = dict(STEP1_COMP_CHAR)
STEP2_COMP_CHAR["J"] = "1"


# Hand model
@dataclass
class Hand:
    strength: int  # Hand strength, determined by cards combination
    comp_str: str  # Representative string for comparison for equivalent strength
    bid: int  # Hand bid for final result

    def __eq__(self, other):
        return (self.strength == other.strength) and (self.comp_str == other.comp_str)

    def __gt__(self, other):
        return (self.strength > other.strength) or ((self.strength == other.strength) and (self.comp_str > other.comp_str))

    def __ge__(self, other):
        return (self.strength >= other.strength) or ((self.strength == other.strength) and (self.comp_str >= other.comp_str))

    def __lt__(self, other):
        return (self.strength < other.strength) or ((self.strength == other.strength) and (self.comp_str < other.comp_str))

    def __le__(self, other):
        return (self.strength <= other.strength) or ((self.strength == other.strength) and (self.comp_str <= other.comp_str))


class D07Puzzle(AOCPuzzle, ABC):
    def __init__(self, input_file: Path):
        self.hands = []
        super().__init__(input_file)

    @abstractmethod
    def mapping(self) -> Dict[str, str]:  # pragma: no cover
        pass

    def post_process(self, hand_map: Dict[str, int], strength: int) -> int:
        return strength

    def reckon_strength(self, hand_map: Dict[str, int]) -> int:
        hand_len = len(hand_map)
        if hand_len == 5:
            # 5 different cards
            return 1
        elif hand_len == 4:
            # one pair
            return 2
        elif hand_len == 3:
            if any(v == 3 for v in hand_map.values()):
                # three of a kind (3+1+1)
                return 4
            else:
                # two pairs (2+2+1)
                return 3
        elif hand_len == 2:
            if any(v == 4 for v in hand_map.values()):
                # four of a kind (4+1)
                return 6
            else:
                # full house (3+2)
                return 5
        elif hand_len == 1:
            # five of a kind
            return 7
        return 0

    def parse_line(self, index: int, line: str) -> str:
        # Parse hand
        line = super().parse_line(index, line)
        m = HAND_PATTERN.match(line)
        if m:  # pragma: no branch
            hand = m.group(1)
            bid = int(m.group(2))

            # Iterate on cards
            comp_str = ""
            hand_map = {}
            for c in hand:
                # Build representative string
                comp_str += self.mapping()[c]

                # Build representative map
                if c in hand_map:
                    hand_map[c] += 1
                else:
                    hand_map[c] = 1

            # Reckon strength
            strength = self.reckon_strength(hand_map)

            # Post-process strength
            strength = self.post_process(hand_map, strength)

            # New hand
            h = Hand(strength, comp_str, bid)
            self.hands.append(h)
            logging.info(f"Parsed hand: {h}")

    def solve(self) -> int:
        # Sort list of hands
        sorted_hands = sorted(self.hands)
        logging.info(f"sorted hands: {sorted_hands}")
        out = 0
        for rank, h in enumerate(sorted_hands, start=1):
            out += rank * h.bid
        return out


class D07Step1Puzzle(D07Puzzle):
    def mapping(self) -> Dict[str, str]:
        return STEP1_COMP_CHAR


class D07Step2Puzzle(D07Puzzle):
    def mapping(self) -> Dict[str, str]:
        return STEP2_COMP_CHAR

    def post_process(self, hand_map: Dict[str, int], strength: int) -> int:
        hand_len = len(hand_map)
        if "J" in hand_map and 1 < hand_len:
            # Specific Joker process
            inv_hand_map = {v: k for k, v in hand_map.items() if k != "J"}
            jokers_nb = hand_map["J"]
            max_others = max(inv_hand_map.keys())
            upgraded_card = inv_hand_map[max_others]
            hand_map[upgraded_card] += jokers_nb
            del hand_map["J"]
            return self.reckon_strength(hand_map)
        return strength
