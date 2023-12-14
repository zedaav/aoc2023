from aoc2023.day14 import D14Step1Puzzle, D14Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD14(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D14Step1Puzzle, "d14.sample.txt", 136)

    def test_step1_input(self):
        self.check_solution(D14Step1Puzzle, "d14.input.txt", 106517)

    def test_step2_sample(self):
        self.check_solution(D14Step2Puzzle, "d14.sample.txt", 64)

    def test_step2_input(self):
        self.check_solution(D14Step2Puzzle, "d14.input.txt", 79723)
