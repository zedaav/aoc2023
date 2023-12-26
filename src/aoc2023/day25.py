import logging
import re
from pathlib import Path

from networkx import Graph, node_connected_component, shortest_path_length

from aoc2023.puzzle import AOCPuzzle

"""
Solutions for https://adventofcode.com/2023/day/25
"""

# Components graph pattern
COMPONENT_PATTERN = re.compile("([a-z]+): ([a-z ]+)")


class D25Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        self.graph = Graph()
        super().__init__(input_file)

        # Count things
        logging.info(f"Found components: {len(self.graph)}")

    def parse_line(self, index: int, line: str) -> str:
        # Add nodes and edges to the graph
        line = super().parse_line(index, line)
        m = COMPONENT_PATTERN.match(line)
        assert m is not None
        comp_a = m.group(1)
        for comp_b in m.group(2).split(" "):
            self.graph.add_edge(comp_a, comp_b)


class D25Step1Puzzle(D25Puzzle):
    def solve(self) -> int:
        # Iterate on edges to find cost for shortest path between nodes with broken link
        costs = []
        for edge in self.graph.edges:
            self.graph.remove_edge(*edge)
            costs.append((edge, shortest_path_length(self.graph, *edge)))
            self.graph.add_edge(*edge)

        # Sort to get the top 3 cost
        costs = sorted(costs, key=lambda n: n[1], reverse=True)

        # Remove this top 3 edges
        for i in range(3):
            logging.info(f"removing edge {costs[i][0]} (cost {costs[i][1]})")
            self.graph.remove_edge(*costs[i][0])

        # Get two groups of components, based on first component pair for which the link was broken
        group1_len = len(node_connected_component(self.graph, costs[0][0][0]))
        group2_len = len(node_connected_component(self.graph, costs[0][0][1]))
        logging.info(f"2 groups found of size {group1_len} and {group2_len}")
        assert group1_len < len(self.graph)
        assert group2_len < len(self.graph)
        assert group1_len + group2_len == len(self.graph)
        return group1_len * group2_len
