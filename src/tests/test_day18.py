from aoc2023.day18 import D18Step1Puzzle, D18Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD18(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D18Step1Puzzle, "d18.sample.txt", 62)

    def test_step1_input(self):
        self.check_solution(D18Step1Puzzle, "d18.input.txt", 46359)

    def test_step2_sample(self):
        self.check_solution(D18Step2Puzzle, "d18.sample.txt", 952408144115)

    def test_step2_input(self):
        self.check_solution(D18Step2Puzzle, "d18.input.txt", 59574883048274)
