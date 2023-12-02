from aoc2023.day02 import D02Step1Puzzle, D02Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD02(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D02Step1Puzzle, "d02.sample.txt", 8)

    def test_step1_input(self):
        self.check_solution(D02Step1Puzzle, "d02.input.txt", 2268)

    def test_step2_sample(self):
        self.check_solution(D02Step2Puzzle, "d02.sample.txt", 2286)

    def test_step2_input(self):
        self.check_solution(D02Step2Puzzle, "d02.input.txt", 63542)
