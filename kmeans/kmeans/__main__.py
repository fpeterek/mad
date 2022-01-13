import random
import csv

import click
import matplotlib.pyplot as plt

from kmeans import kmeans


def rand_point(max_x: int, max_y: int) -> tuple[int, int]:
    return random.randint(0, max_x), random.randint(0, max_y)


def gen_random(max_x: int = 999, max_y: int = 999, num_points: int = 999) -> list[tuple[int, int]]:
    return [rand_point(max_x, max_y) for _ in range(num_points)]


def load_iris(filename: str) -> list[tuple]:
    with open(filename, newline='') as file:
        reader = csv.reader(file, delimiter=';')
        filtered = filter(lambda item: item and item[0][0].isdigit(), reader)
        sepal_sizes = map(lambda item: (item[0].replace(',', '.'), item[1].replace(',', '.')), filtered)
        numeric_size = map(lambda item: (float(item[0]), float(item[1])), sepal_sizes)
        return list(numeric_size)


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


@click.command()
@click.option('--iris', default='in/iris.csv', help='Path to Iris dataset')
@click.option('--clusters', default=10, help='Number of clusters to find')
@click.option('--attempts', default=10, help='Number of clustering attempts')
def run_iris(iris, clusters, attempts):
    points = load_iris(iris)
    clusters = kmeans(points, clusters, attempts)
    plot(clusters)


@click.command()
@click.option('--max-x', default=1000, help='Max x coordinate')
@click.option('--max-y', default=1000, help='Max y coordinate')
@click.option('--points', default=1000, help='Number of randomly generated points')
@click.option('--clusters', default=10, help='Number of clusters to find')
@click.option('--attempts', default=10, help='Number of clustering attempts')
def run_random(max_x: int, max_y: int, points: int, clusters: int, attempts: int) -> None:
    points = gen_random(max_x, max_y, points)
    clusters = kmeans(points, clusters, attempts)
    plot(clusters)


@click.group(help='Kmeans implementation')
def main() -> None:
    pass


main.add_command(run_random)
main.add_command(run_iris)


if __name__ == '__main__':
    main()
