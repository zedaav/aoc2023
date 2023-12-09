from aoc2023.day09 import D09Step1Puzzle, D09Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD09(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D09Step1Puzzle, "d09.sample.txt", 114)

    def test_step1_input(self):
        self.check_solution(D09Step1Puzzle, "d09.input.txt", 1972648895)

    def test_step2_sample(self):
        self.check_solution(D09Step2Puzzle, "d09.sample.txt", 2)

    def test_step2_input(self):
        self.check_solution(D09Step2Puzzle, "d09.input.txt", 919)
