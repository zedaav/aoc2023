from aoc2023.day00 import D00Step1Puzzle, D00Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD00(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D00Step1Puzzle, "d00.sample.txt", 0)

    def test_step1_input(self):
        self.check_solution(D00Step1Puzzle, "d00.input.txt", 0)

    def test_step2_sample(self):
        self.check_solution(D00Step2Puzzle, "d00.sample.txt", 0)

    def test_step2_input(self):
        self.check_solution(D00Step2Puzzle, "d00.input.txt", 0)
