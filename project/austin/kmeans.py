import random

from geo_point import GeoPoint


def dist_square(p1: GeoPoint, p2: GeoPoint) -> float:
    return calc_dist(p1, p2) ** 2


def calc_dist(p1: GeoPoint, p2: GeoPoint) -> float:
    return p1.distance(p2)


def calc_centroids(clusters) -> list[tuple[float, float]]:
    centroids = []
    for cluster in clusters:
        sum_x = 0
        sum_y = 0
        for point in cluster:
            sum_x += point[0]
            sum_y += point[1]
        centroids.append((sum_x / len(cluster), sum_y / len(cluster)))
    return centroids


def distribute_points(centroids, points) -> list[list[GeoPoint]]:
    clusters = [[] for _ in range(len(centroids))]
    for point in points:
        min_centroid = 0
        min_dist = None
        for idx, centroid in enumerate(centroids):
            dist = calc_dist(point, centroid)
            if min_dist is None or dist < min_dist:
                min_dist = dist
                min_centroid = idx
        clusters[min_centroid].append(point)

    return clusters


def run_iteration(points: list[GeoPoint], cluster_count: int):
    centroids = random.sample(points, cluster_count)
    max_iterations = 10
    for i in range(max_iterations):
        clusters = distribute_points(centroids, points)
        new_centroids = calc_centroids(clusters)
        if new_centroids == centroids:
            break
        centroids = new_centroids

    return centroids, clusters


def calc_dist_sse(centroids, clusters):
    distances = 0
    for centroid, cluster in zip(centroids, clusters):
        for point in cluster:
            distances += dist_square(centroid, point)
    return distances


def kmeans(points: list[GeoPoint], cluster_count: int, attempts: int) -> list[list[GeoPoint]]:
    best_sse = None
    best_distribution = None
    for i in range(attempts):
        centroids, clusters = run_iteration(points, cluster_count)
        sse = calc_dist_sse(centroids, clusters)
        if best_sse is None or sse < best_sse:
            best_sse = sse
            best_distribution = clusters
    return best_distribution

