from aoc2023.day24 import D24Step1Puzzle, D24Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD24(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D24Step1Puzzle, "d24.sample.txt", 2, (7, 27))

    def test_step1_input(self):
        self.check_solution(D24Step1Puzzle, "d24.input.txt", 29142, (200000000000000, 400000000000000))

    def test_step2_sample(self):
        self.check_solution(D24Step2Puzzle, "d24.sample.txt", 47)

    def test_step2_input(self):
        self.check_solution(D24Step2Puzzle, "d24.input.txt", 848947587263033)
