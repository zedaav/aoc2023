from aoc2023.day08 import D08Step1Puzzle, D08Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD08(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D08Step1Puzzle, "d08.sample.txt", 2)
        self.check_solution(D08Step1Puzzle, "d08.sample2.txt", 6)

    def test_step1_input(self):
        self.check_solution(D08Step1Puzzle, "d08.input.txt", 23147)

    def test_step2_sample(self):
        self.check_solution(D08Step2Puzzle, "d08.sample3.txt", 6)

    def test_step2_input(self):
        self.check_solution(D08Step2Puzzle, "d08.input.txt", 22289513667691)
