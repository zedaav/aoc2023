from pathlib import Path

from pytest_multilog import TestHelper

from aoc2023.puzzle import AOCPuzzle


# Base class for AOC puzzles tests
class AOCPuzzleTester(TestHelper):
    INPUTS_ROOT = Path(__file__).parent / "inputs"

    # Access to input file
    def get_input(self, name: str) -> Path:
        return self.INPUTS_ROOT / name

    # Test puzzle solution
    def check_solution(self, puzzle: AOCPuzzle, input_name: str, expected_solution: int, solve_arg=None):
        # Solve puzzle
        p = puzzle(self.get_input(input_name))
        solution = p.solve() if solve_arg is None else p.solve(solve_arg)

        # Verify solution
        assert solution == expected_solution, f"Solution not found (expected: {expected_solution} / found: {solution})"
