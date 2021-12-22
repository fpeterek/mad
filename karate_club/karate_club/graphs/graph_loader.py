from typing import TextIO


def load_nodes_and_edges(file: TextIO) -> tuple[set[int], set[tuple[int, int]]]:
    nodes: set[int] = set()
    edges: set[tuple[int, int]] = set()

    for line in file:
        if line:
            split = line.split(';')
            n1, n2 = int(split[0]), int(split[1])
            edges.add((n1, n2))
            nodes.add(n1)
            nodes.add(n2)

    return nodes, edges


def load_file(filename: str) -> tuple[set[int], set[tuple[int, int]]]:
    with open(filename) as file:
        return load_nodes_and_edges(file)
