import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import reduce
from math import gcd
from pathlib import Path
from typing import Dict, List

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/8
"""

# Instructions pattern
INSTRUCTION_PATTERN = re.compile("([RL]+)")

# Nodes pattern
NODES_PATTERN = re.compile("([A-Z1-9]{3}) = \\(([A-Z1-9]{3}), ([A-Z1-9]{3})\\)")


@dataclass
class Node:
    name: str
    left: str
    right: str


class D08Puzzle(AOCPuzzle, ABC):
    def __init__(self, input_file: Path):
        self.instructions = None
        self.nodes: Dict[str, Node] = {}
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        line = super().parse_line(index, line)
        if self.instructions is None:
            self.instructions = INSTRUCTION_PATTERN.match(line).group(1)
        else:
            m = NODES_PATTERN.match(line)
            if m is not None:
                name = m.group(1)
                self.nodes[name] = Node(name, m.group(2), m.group(3))
                logging.info(f"New node: {self.nodes[name]}")

    @abstractmethod
    def start_nodes(self) -> List[str]:  # pragma: no cover
        pass

    @abstractmethod
    def is_complete(self, seq: List[str]) -> bool:  # pragma: no cover
        pass

    def build_seqs(self):
        # Iterate from start to end conditions
        node_sequences = [[n] for n in self.start_nodes()]
        steps = 0
        while not all(self.is_complete(seq) for seq in node_sequences):
            next_move = self.instructions[steps % len(self.instructions)]  # NOQA: S001

            # Make all sequences progress (until they are completed)
            for seq in filter(lambda seq: not self.is_complete(seq), node_sequences):
                last_node = seq[-1]
                next_node = self.nodes[last_node].left if next_move == "L" else self.nodes[last_node].right
                seq.append(next_node)
            steps += 1
        return node_sequences


class D08Step1Puzzle(D08Puzzle):
    def start_nodes(self) -> List[str]:
        return ["AAA"]

    def is_complete(self, seq: List[str]) -> bool:
        return seq[-1] == "ZZZ"

    def solve(self) -> int:
        seqs = self.build_seqs()
        return len(seqs[0]) - 1  # Don't count first node


# Custom multiple gcd (doesn't exist < 3.9)
def my_lcm_base(x, y):
    return (x * y) // gcd(x, y)


# Custom lcm (doesn't exist < 3.9)
def my_lcm(*numbers):
    return reduce(my_lcm_base, numbers, 1)


class D08Step2Puzzle(D08Puzzle):
    def start_nodes(self) -> List[str]:
        return [n for n in self.nodes.keys() if n.endswith("A")]

    def is_complete(self, seq: List[str]) -> bool:
        return (len(seq) > 1) and seq[-1].endswith("Z")

    def solve(self) -> int:
        seqs = self.build_seqs()
        all_lengths = [len(seq) - 1 for seq in seqs]
        return my_lcm(*all_lengths)
