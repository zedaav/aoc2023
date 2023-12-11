from aoc2023.day11 import D11Puzzle
from tests.base import AOCPuzzleTester


class TestD11(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D11Puzzle, "d11.sample.txt", 374, 2)

    def test_step1_input(self):
        self.check_solution(D11Puzzle, "d11.input.txt", 9543156, 2)

    def test_step2_sample(self):
        self.check_solution(D11Puzzle, "d11.sample.txt", 8410, 100)

    def test_step2_input(self):
        self.check_solution(D11Puzzle, "d11.input.txt", 625243292686, 1000000)
