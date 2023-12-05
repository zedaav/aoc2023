from aoc2023.day05 import D05Step1Puzzle, D05Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD05(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D05Step1Puzzle, "d05.sample.txt", 35)

    def test_step1_input(self):
        self.check_solution(D05Step1Puzzle, "d05.input.txt", 178159714)

    def test_step2_sample(self):
        self.check_solution(D05Step2Puzzle, "d05.sample.txt", 46)

    def test_step2_input(self):
        self.check_solution(D05Step2Puzzle, "d05.input.txt", 100165128)
