from aoc2023.day25 import D25Step1Puzzle
from tests.base import AOCPuzzleTester


class TestD25(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D25Step1Puzzle, "d25.sample.txt", 54)

    def test_step1_input(self):
        self.check_solution(D25Step1Puzzle, "d25.input.txt", 556467)
