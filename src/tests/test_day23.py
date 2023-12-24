from aoc2023.day23 import D23Step1Puzzle, D23Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD23(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D23Step1Puzzle, "d23.sample.txt", 94)

    def test_step1_input(self):
        self.check_solution(D23Step1Puzzle, "d23.input.txt", 2162)

    def test_step2_sample(self):
        self.check_solution(D23Step2Puzzle, "d23.sample.txt", 154)

    def test_step2_input(self):
        self.check_solution(D23Step2Puzzle, "d23.input.txt", 6334)
