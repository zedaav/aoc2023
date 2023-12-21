from aoc2023.day20 import D20Step1Puzzle, D20Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD20(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D20Step1Puzzle, "d20.sample.txt", 32000000)
        self.check_solution(D20Step1Puzzle, "d20.sample2.txt", 11687500)

    def test_step1_input(self):
        self.check_solution(D20Step1Puzzle, "d20.input.txt", 794930686)

    def test_step2_input(self):
        self.check_solution(D20Step2Puzzle, "d20.input.txt", 0)
