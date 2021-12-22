from typing import Optional

import graphs.graph_loader as gl


class Graph:
    def __init__(self, nodes: set[int], edges: set[tuple[int, int]]):
        self.matrix = [[0] * len(nodes) for _ in nodes]
        for node1, node2 in edges:
            self.matrix[node1-1][node2-1] = 1
            self.matrix[node2-1][node1-1] = 1

    def __str__(self):
        str_matrix = map(lambda line: map(str, line), self.matrix)
        return '\n'.join(map(' '.join, str_matrix))

    def to_dist_matrix(self):
        dist = [[1 if val else None for val in line] for line in self.matrix]

        for i in range(len(dist)):
            for j in range(len(dist)):
                for k in range(len(dist)):
                    if j == k:
                        dist[j][k] = 0
                        continue

                    if dist[j][i] is None or dist[i][k] is None:
                        continue

                    dist_sum = dist[j][i] + dist[i][k]
                    if dist[j][k] is None or dist[j][k] > dist_sum:
                        dist[j][k] = dist_sum

        return DistanceMatrix(dist)

    @staticmethod
    def load_from_file(filename: str):
        nodes, edges = gl.load_file(filename)
        return Graph(nodes=nodes, edges=edges)


class DistanceMatrix(Graph):
    def __init__(self, matrix: list[list[int]]):
        super().__init__(set(), set())
        self.matrix = matrix

    def to_dist_matrix(self):
        raise ValueError("Matrix is already a distance matrix")

    def avg_dist(self) -> float:
        dist_sum = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if not self.matrix[i][j]:
                    continue
                dist_sum += self.matrix[i][j]

        return dist_sum / (len(self.matrix)**2 - len(self.matrix))

    def max_dist(self) -> Optional[int]:
        max_d = None
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if i == j or self.matrix[i][j] is None:
                    continue
                if max_d is None or self.matrix[i][j] > max_d:
                    max_d = self.matrix[i][j]

        return max_d

    def diameter(self) -> int:
        return self.max_dist()

    def avg_dist_for_node(self, node_id) -> float:
        node = node_id - 1
        line = self.matrix[node]
        dist_sum = 0
        for i in range(len(self.matrix)):
            if not line[i]:
                continue
            dist_sum += line[i]
        return dist_sum / len(self.matrix)

    def closeness_centrality(self, node_id) -> float:
        return self.avg_dist_for_node(node_id) ** -1

    def closeness_centralities(self) -> dict[int, float]:
        return {node_id: self.closeness_centrality(node_id) for node_id in range(1, len(self.matrix) + 1)}
