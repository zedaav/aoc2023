from aoc2023.day07 import D07Step1Puzzle, D07Step2Puzzle
from tests.base import AOCPuzzleTester


class TestD07(AOCPuzzleTester):
    def test_step1_sample(self):
        self.check_solution(D07Step1Puzzle, "d07.sample.txt", 6440)

    def test_step1_input(self):
        self.check_solution(D07Step1Puzzle, "d07.input.txt", 249726565)

    def test_step2_sample(self):
        self.check_solution(D07Step2Puzzle, "d07.sample.txt", 5905)

    def test_step2_input(self):
        self.check_solution(D07Step2Puzzle, "d07.input.txt", 251135960)
