from aoc2023.day03 import D03Step1Puzzle, D03Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD03(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D03Step1Puzzle, "d03.sample.txt", 4361)

    def test_step1_input(self):
        self.check_solution(D03Step1Puzzle, "d03.input.txt", 532331)

    def test_step2_sample(self):
        self.check_solution(D03Step2Puzzle, "d03.sample.txt", 467835)

    def test_step2_input(self):
        self.check_solution(D03Step2Puzzle, "d03.input.txt", 82301120)
