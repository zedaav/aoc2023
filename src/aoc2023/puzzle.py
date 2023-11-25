from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union


# Base class for puzzle solutions
class AOCPuzzle(ABC):
    def __init__(self, input_file: Path):
        # Parse input file
        self.input_file = input_file
        self.input_lines = []
        self.parse_file()

    def parse_file(self):
        # Check file existence
        assert self.input_file.is_file(), f"File not found: {self.input_file}"

        # Browse input lines
        with self.input_file.open() as f:
            for index, line in enumerate(f.readlines(), start=1):
                # Remember parsed line
                self.input_lines.append(self.parse_line(index, line))

    def parse_line(self, index: int, line: str) -> str:
        # Default implementation: just strip meaningless characters at end of line
        return line.strip("\r\n ")

    @abstractmethod
    def solve(self) -> Union[int, str, List[str]]:  # pragma: no cover
        pass
