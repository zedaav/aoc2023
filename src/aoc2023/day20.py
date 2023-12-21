import logging
import re
from dataclasses import dataclass, field
from math import lcm
from pathlib import Path
from typing import Dict, List, Tuple

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/20
"""

# Modules mapping pattern
MODULES_PATTERN = re.compile("([%&])?([a-z]+) +-> +([a-z, ]+)")


# Pulse stack handler
@dataclass
class PulseStack:
    stack: List[Tuple[object, str, bool]] = field(default_factory=list)
    low_count: int = 0
    high_count: int = 0

    def add_to_stack(self, target: object, source: str, pulse: bool):
        if pulse:
            self.high_count += 1
        else:
            self.low_count += 1
        self.stack.append((target, source, pulse))


# Base module model
@dataclass
class Module:
    name: str
    outputs_names: List[str]
    outputs: List[object] = field(default_factory=list)
    inputs: List[object] = field(default_factory=list)

    def handle_pulse(self, source: str, pulse: bool, pulse_stack: PulseStack):
        # Default implementation
        pass

    def add_input(self, module: object):
        self.inputs.append(module)

    def propagate(self, pulse: bool, pulse_stack: PulseStack):
        for m in self.outputs:
            pulse_stack.add_to_stack(m, self.name, pulse)

    def get_state(self) -> str:
        # Default: no state
        return ""

    def reset(self):
        # Reset state: nothing to do by default
        pass


# Broadcaster module
class BroadcasterModule(Module):
    def handle_pulse(self, source: str, pulse: bool, pulse_stack: PulseStack):
        # Distribute to all outputs
        self.propagate(pulse, pulse_stack)


# Flip-flop module
@dataclass
class FlipFlopModule(Module):
    state: bool = False

    def handle_pulse(self, source: str, pulse: bool, pulse_stack: PulseStack):
        if pulse:
            # High pulse: nothing to do
            pass
        else:
            # Low pulse: switch state
            self.state = not self.state

            # Propagate
            self.propagate(self.state, pulse_stack)

    def get_state(self) -> str:
        # Internal state
        return str(self.state)

    def reset(self):
        self.state = False


# Conjunction module
@dataclass
class ConjunctionModule(Module):
    input_states: Dict[str, bool] = field(default_factory=dict)

    def handle_pulse(self, source: str, pulse: bool, pulse_stack: PulseStack):
        # Update input states
        self.input_states[source] = pulse

        # Send pulse to outputs
        out_pulse = False if all(p for p in self.input_states.values()) else True
        self.propagate(out_pulse, pulse_stack)

    def add_input(self, module: object):
        super().add_input(module)
        self.input_states[module.name] = False

    def get_state(self) -> str:
        # Internal state
        return str(self.input_states)

    def reset(self):
        for k in self.input_states.keys():
            self.input_states[k] = False


# Fake button module
class ButtonModule(Module):
    def handle_pulse(self, source: str, pulse: bool, pulse_stack: PulseStack):
        # Distribute False to all outputs
        self.propagate(False, pulse_stack)


class D20Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.modules: Dict[str, Module] = {}
        super().__init__(input_file)

        # Append fake button module
        self.modules["button"] = ButtonModule("button", ["broadcaster"], [], [])

        # Add missing outputs
        missing_modules = {}
        for m in self.modules.values():
            for output in m.outputs_names:
                # Handle unknown modules as basic modules
                if output not in self.modules:
                    new_m = self.create_module("", output, [])
                    logging.info(f"New missing module (from outputs): {new_m}")
                    missing_modules[output] = new_m
        self.modules.update(missing_modules)

        # Reconcile modules with their outputs
        for m in self.modules.values():
            for output in m.outputs_names:
                # Add link (both ways)
                m.outputs.append(self.modules[output])
                self.modules[output].add_input(m)

    def create_module(self, mod_type: str, name: str, output_names: List[str]) -> Module:
        if mod_type == "%":
            return FlipFlopModule(name, output_names)
        if mod_type == "&":
            return ConjunctionModule(name, output_names)
        if name == "broadcaster":
            return BroadcasterModule(name, output_names)
        return Module(name, output_names)

    def parse_line(self, index: int, line: str) -> str:
        # Super call to get line
        line = super().parse_line(index, line)
        m = MODULES_PATTERN.match(line)
        assert m is not None
        mod_type, name, output_names = m.group(1), m.group(2), m.group(3).split(", ")
        m = self.create_module(mod_type, name, output_names)
        logging.info(f"New module: {m}")
        self.modules[name] = m

    def get_all_states(self) -> str:
        state_str = ""
        for m in self.modules.values():
            state_str += f"{m.name}:{m.get_state()};"
        return state_str


class D20Step1Puzzle(D20Puzzle):
    def solve(self) -> int:
        pulse_stack = PulseStack()
        push_max_count = 1000
        modules_states = {}

        # Push button until getting a repeating state pattern
        m_state = self.get_all_states()
        pos = 0
        while self.get_all_states() not in modules_states and (pos < push_max_count):
            modules_states[m_state] = pos
            pos += 1

            logging.info(f"--> Push button! ({pos})")
            self.modules["button"].handle_pulse(None, False, pulse_stack)
            while pulse_stack.stack:
                target, source, pulse = pulse_stack.stack.pop(0)
                target.handle_pulse(source, pulse, pulse_stack)

            m_state = self.get_all_states()

        total_pulse = pulse_stack.high_count * pulse_stack.low_count
        logging.info(f"repeating state found after {pos} button push; pulse count for one pattern: {total_pulse}")
        if pos < push_max_count:
            assert modules_states[m_state] == 0

        # How many patterns over 1000?
        pattern_size = len(modules_states)
        patterns_count = ((push_max_count - pattern_size) // pattern_size) + 1
        logging.info(f"total: {patterns_count} repeating patterns (including first one)")
        total_pulse *= patterns_count * patterns_count

        # Remaining pulse push
        remaining_pushes = push_max_count - (patterns_count * pattern_size)
        logging.info(f"still {remaining_pushes} button push to do")

        return total_pulse


class D20Step2Puzzle(D20Puzzle):
    def solve(self) -> int:
        # Go from output
        rx = self.modules["rx"]

        # Only one input for rx, and this is a conjunction
        assert len(rx.inputs) == 1
        conj: ConjunctionModule = rx.inputs[0]
        assert isinstance(conj, ConjunctionModule)

        # Expect all inputs of this conjunction to be conjunctions as well
        assert all(isinstance(m, ConjunctionModule) for m in conj.inputs)

        # Find all button push counts for level 1 inputs are high --> rx receives low
        inputs_pushes = []
        for conj_input in conj.inputs:
            # Reset all modules
            for m in self.modules.values():
                m.reset()

            # Iterate on button pushes, until getting high pulse for this input
            pulse_stack = PulseStack()
            pushes = 0
            go_on = True
            while go_on:
                pushes += 1
                self.modules["button"].handle_pulse(None, False, pulse_stack)
                while pulse_stack.stack:
                    target, source, pulse = pulse_stack.stack.pop(0)
                    target.handle_pulse(source, pulse, pulse_stack)
                    if source == conj_input.name and target.name == conj.name and pulse:
                        go_on = False
                        break
            inputs_pushes.append(pushes)

        # Then return lcm of them
        return lcm(*inputs_pushes)
