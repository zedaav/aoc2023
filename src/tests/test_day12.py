from aoc2023.day12 import D12Step1Puzzle, D12Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD12(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D12Step1Puzzle, "d12.sample.txt", 21)

    def test_step1_input(self):
        self.check_solution(D12Step1Puzzle, "d12.input.txt", 7633)

    def test_step2_sample(self):
        self.check_solution(D12Step2Puzzle, "d12.sample.txt", 525152)

    def test_step2_input(self):
        self.check_solution(D12Step2Puzzle, "d12.input.txt", 23903579139437)
