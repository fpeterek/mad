import random

import kmeans.kmeans_setup as ks
import kmeans.kmeans_core as kc
import kmeans.kmeans_distribution as kd
from data.geo_point import GeoPoint


def run_iteration(points: list[GeoPoint], cluster_count: int, processes: int):
    centroids = random.sample(points, cluster_count)
    max_iterations = 10
    dist_fn = [kd.distribute_in_serial, kd.distribute_in_parallel][processes > 1]
    centroid_fn = [kd.calc_centroids_in_serial, kd.calc_centroids_in_parallel][processes > 1]

    for i in range(max_iterations):
        clusters = dist_fn(centroids, points, processes)
        new_centroids = centroid_fn(clusters)
        if new_centroids == centroids:
            break
        centroids = new_centroids

    return centroids, clusters


def kmeans(points: list[GeoPoint], cluster_count: int, attempts: int, processes: int) -> list[list[GeoPoint]]:
    best_sse = None
    best_distribution = None

    ks.setup(points, processes)
    pool = kd.create_processes(processes) if processes > 1 else None

    for i in range(attempts):
        centroids, clusters = run_iteration(points, cluster_count, processes)
        sse = kc.calc_dist_sse(centroids, clusters)
        if best_sse is None or sse < best_sse:
            best_sse = sse
            best_distribution = clusters

    ks.shutdown(pool)

    return best_distribution

