from collections import Counter
from typing import Iterable

import graphs.graph_loader as gl


class Graph:

    class Node:
        def __init__(self, node_id: int):
            self.id = node_id
            self.links = set()

        def add_link(self, node):
            self.links.add(node)

        def __hash__(self):
            # IDs should be unique, thus, we can afford to hash by ids
            return hash(self.id)

        def __str__(self):
            return f'Node {{id={self.id}, links=[{", ".join(map(lambda n: str(n.id), self.links))}]}}'

        def degree(self) -> int:
            return len(self.links)

    def __init__(self, nodes: set[int], edges: set[tuple[int, int]]):
        self.nodes = {node_id: Graph.Node(node_id) for node_id in nodes}
        for id1, id2 in edges:
            node1 = self[id1]
            node2 = self[id2]
            node1.add_link(node2)
            node2.add_link(node1)

    def get_node(self, node_id: int):
        return self.nodes[node_id]

    @property
    def __degrees(self) -> Iterable[int]:
        return map(Graph.Node.degree, self.nodes.values())

    def max_degree(self) -> int:
        return max(self.__degrees)

    def min_degree(self) -> int:
        return min(self.__degrees)

    def avg_degree(self) -> float:
        degrees = list(self.__degrees)
        return sum(degrees) / len(degrees)

    def degree_counter(self) -> Counter:
        return Counter(self.__degrees)

    def relative_degree_counter(self) -> dict[int, float]:
        counter = self.degree_counter()
        relative = dict()
        node_count = len(self.nodes)

        for degree, count in counter.items():
            relative[degree] = count / node_count

        return relative

    def __getitem__(self, node_id):
        return self.nodes[node_id]

    def __str__(self):
        return '\n'.join(map(str, self.nodes.values()))

    @staticmethod
    def load_from_file(filename: str):
        nodes, edges = gl.load_file(filename)
        return Graph(nodes=nodes, edges=edges)
