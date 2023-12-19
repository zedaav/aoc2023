import logging
import re
from dataclasses import dataclass
from math import prod
from pathlib import Path
from typing import Dict, List, Tuple

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/19
"""

# Workflow line
WORKFLOW_PATTERN = re.compile(r"([a-z]+)\{(.+)\}")

# Instruction inside workflow
INSTRUCTION_PATTERN = re.compile(r",?(([xmas])([<>])([0-9]+):)?([a-zAR]+)")

# Part definition
PART_PATTERN = re.compile(r"\{x=([0-9]+),m=([0-9]+),a=([0-9]+),s=([0-9]+)\}")


@dataclass
class Instruction:
    prop_name: str
    operator: str
    value: int
    target_group: str


@dataclass
class Workflow:
    src_group: str
    instructions: List[Instruction]
    default_group: str


class D19Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.workflows: Dict[str, Workflow] = {}
        self.parts: List[Dict[str, Tuple[int, int]]] = []
        super().__init__(input_file)

    def parse_line(self, index: int, line: str) -> str:
        # Super call to get line
        line = super().parse_line(index, line)

        # Try to match workflow
        m = WORKFLOW_PATTERN.match(line)
        if m is not None:
            src_group = m.group(1)
            instructions = []
            for n in re.finditer(INSTRUCTION_PATTERN, m.group(2)):
                if n.group(1) is not None:
                    prop_name = n.group(2)
                    operator = n.group(3)
                    assert operator in ["<", ">"]
                    value = int(n.group(4))
                    target_group = n.group(5)
                    instructions.append(Instruction(prop_name, operator, value, target_group))
                else:
                    default_group = n.group(5)
            self.workflows[src_group] = Workflow(src_group, instructions, default_group)
            logging.info(f"Parsed workflow: {self.workflows[src_group]}")
        else:
            # Try to parse part
            m = PART_PATTERN.match(line)
            if m is not None:
                self.parts.append(
                    {
                        "x": (int(m.group(1)), int(m.group(1))),
                        "m": (int(m.group(2)), int(m.group(2))),
                        "a": (int(m.group(3)), int(m.group(3))),
                        "s": (int(m.group(4)), int(m.group(4))),
                    }
                )
                logging.info(f"Parsed part: {self.parts[-1]}")

    def accepted(self, input_parts: List[Dict[str, Tuple[int, int]]]) -> List[Dict[str, Tuple[int, int]]]:
        # Iterate on parts
        pending_parts = list(input_parts)
        accepted_parts: List[Dict[str, Tuple[int, int]]] = []
        while pending_parts:
            # Process workflows
            part = pending_parts.pop(0)
            current_workflow = "in"
            while current_workflow not in ["A", "R"]:
                # Iterate on instructions
                w = self.workflows[current_workflow]
                for instruction in w.instructions:
                    min_v, max_v = part[instruction.prop_name]
                    if ((instruction.operator == ">") and (min_v > instruction.value)) or ((instruction.operator == "<") and (max_v < instruction.value)):
                        # Condition match, continue with next workflow
                        current_workflow = instruction.target_group
                        break

                    if min_v < instruction.value < max_v:
                        # New part with excluded range: recursive process on accepted parts for this one
                        new_part = dict(part)
                        new_part[instruction.prop_name] = (instruction.value, max_v) if (instruction.operator == "<") else (min_v, instruction.value)
                        accepted_parts.extend(self.accepted([new_part]))

                        # Keep part which satisfies the condition
                        part[instruction.prop_name] = (min_v, instruction.value - 1) if (instruction.operator == "<") else (instruction.value + 1, max_v)
                        current_workflow = instruction.target_group
                        break
                else:
                    # None of the conditions are satisfied, go to default
                    current_workflow = w.default_group

            if current_workflow == "A":
                accepted_parts.append(part)

        return accepted_parts


class D19Step1Puzzle(D19Puzzle):
    def solve(self) -> int:
        # Sum all accepted parts properties
        return sum(sum(t[0] for t in p.values()) for p in self.accepted(self.parts))


class D19Step2Puzzle(D19Puzzle):
    def solve(self) -> int:
        accepted = self.accepted([{"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}])
        return sum(prod((t[1] - t[0] + 1) for t in a.values()) for a in accepted)
