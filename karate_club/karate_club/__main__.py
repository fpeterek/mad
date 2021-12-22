import math

import matplotlib.pyplot as plt

from graphs.matrix_graph import Graph as MatrixGraph
from graphs.list_graph import Graph as ListGraph


def graph_test(name):
    def graph_test_decorator(fn):
        def decorated_fn():
            line = '--------------------------------------------------------------------------------------------'
            upper_len = len(line) - len(name) - 2
            left = upper_len // 2
            right = int(math.ceil(upper_len / 2))

            print(f'{"-" * left} {name} {"-" * right}')

            fn()

            print(line)
            print('')

        return decorated_fn

    return graph_test_decorator


@graph_test('Matrix Graph')
def matrix_graph_test():
    graph = MatrixGraph.load_from_file('in/KarateClub.csv')
    print(graph)


def plot_hist(dictionary: dict) -> None:
    plt.bar(list(dictionary.keys()), dictionary.values(), color='r')
    plt.draw()
    plt.show()


@graph_test('List Graph')
def list_graph_test():
    graph = ListGraph.load_from_file('in/KarateClub.csv')
    print(graph)
    print('Graph properties')
    print(f'Min degree: {graph.min_degree()}')
    print(f'Max degree: {graph.max_degree()}')
    print(f'Avg degree: {graph.avg_degree()}')
    plot_hist(graph.degree_counter())
    plot_hist(graph.relative_degree_counter())


def main():
    matrix_graph_test()
    list_graph_test()


if __name__ == '__main__':
    main()
