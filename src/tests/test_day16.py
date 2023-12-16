from aoc2023.day16 import D16Step1Puzzle, D16Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD16(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D16Step1Puzzle, "d16.sample.txt", 46)

    def test_step1_input(self):
        self.check_solution(D16Step1Puzzle, "d16.input.txt", 7482)

    def test_step2_sample(self):
        self.check_solution(D16Step2Puzzle, "d16.sample.txt", 51)

    def test_step2_input(self):
        self.check_solution(D16Step2Puzzle, "d16.input.txt", 7896)
