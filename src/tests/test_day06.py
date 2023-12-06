from aoc2023.day06 import D06Step1Puzzle, D06Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD06(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D06Step1Puzzle, "d06.sample.txt", 288)

    def test_step1_input(self):
        self.check_solution(D06Step1Puzzle, "d06.input.txt", 2756160)

    def test_step2_sample(self):
        self.check_solution(D06Step2Puzzle, "d06.sample.txt", 71503)

    def test_step2_input(self):
        self.check_solution(D06Step2Puzzle, "d06.input.txt", 34788142)
