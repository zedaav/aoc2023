from aoc2023.day04 import D04Step1Puzzle, D04Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD04(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D04Step1Puzzle, "d04.sample.txt", 13)

    def test_step1_input(self):
        self.check_solution(D04Step1Puzzle, "d04.input.txt", 20407)

    def test_step2_sample(self):
        self.check_solution(D04Step2Puzzle, "d04.sample.txt", 30)

    def test_step2_input(self):
        self.check_solution(D04Step2Puzzle, "d04.input.txt", 23806951)
