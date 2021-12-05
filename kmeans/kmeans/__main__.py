import random

import click
import matplotlib.pyplot as plt

from kmeans import kmeans


def rand_point(max_x: int, max_y: int) -> tuple[int, int]:
    return random.randint(0, max_x), random.randint(0, max_y)


def gen_random(max_x: int = 999, max_y: int = 999, num_points: int = 999) -> list[tuple[int, int]]:
    return [rand_point(max_x, max_y) for _ in range(num_points)]


def plot(clusters) -> None:
    figure = plt.figure()
    sub = figure.add_subplot()

    for cluster in clusters:
        xs, ys = [], []
        for point in cluster:
            xs.append(point[0])
            ys.append(point[1])
        sub.scatter(xs, ys, s=10)
    plt.show()


def run(max_x: int, max_y: int, points: int, clusters: int, attempts: int, processes: int) -> None:
    points = gen_random(max_x, max_y, points)
    clusters = kmeans(points, clusters, attempts, processes)
    plot(clusters)


@click.command()
@click.option('--max-x', default=1000, help='Max x coordinate')
@click.option('--max-y', default=1000, help='Max y coordinate')
@click.option('--points', default=1000, help='Number of randomly generated points')
@click.option('--clusters', default=10, help='Number of clusters to find')
@click.option('--attempts', default=10, help='Number of clustering attempts')
@click.option('--processes', default=5, help='Number of processes used when parallelizing the algorithm')
def main(max_x: int, max_y: int, points: int, clusters: int, attempts: int, processes: int) -> None:
    run(max_x-1, max_y-1, points, clusters, attempts, processes)


if __name__ == '__main__':
    main()
