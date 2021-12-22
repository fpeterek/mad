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

    @staticmethod
    def load_from_file(filename: str):
        nodes, edges = gl.load_file(filename)
        return Graph(nodes=nodes, edges=edges)

