from aoc2023.day19 import D19Step1Puzzle, D19Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD19(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D19Step1Puzzle, "d19.sample.txt", 19114)

    def test_step1_input(self):
        self.check_solution(D19Step1Puzzle, "d19.input.txt", 332145)

    def test_step2_sample(self):
        self.check_solution(D19Step2Puzzle, "d19.sample.txt", 167409079868000)

    def test_step2_input(self):
        self.check_solution(D19Step2Puzzle, "d19.input.txt", 136661579897555)
