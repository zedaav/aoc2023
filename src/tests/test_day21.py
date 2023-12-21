from aoc2023.day21 import D21Step1Puzzle, D21Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD21(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D21Step1Puzzle, "d21.sample.txt", 16, 6)

    def test_step1_input(self):
        self.check_solution(D21Step1Puzzle, "d21.input.txt", 3729, 64)

    def test_step2_sample(self):
        self.check_solution(D21Step2Puzzle, "d21.sample.txt", 0)

    def test_step2_input(self):
        self.check_solution(D21Step2Puzzle, "d21.input.txt", 0)
