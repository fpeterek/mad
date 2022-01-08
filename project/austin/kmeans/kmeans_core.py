import kmeans.globals as kg
from data.geo_point import GeoPoint


def dist_square(p1: GeoPoint, p2: GeoPoint) -> float:
    return calc_dist(p1, p2) ** 2


def calc_dist(p1: GeoPoint, p2: GeoPoint) -> float:
    return p1.distance(p2)


def calc_centroid(cluster: list[GeoPoint]) -> GeoPoint:
    sum_x = 0
    sum_y = 0
    for point in cluster:
        sum_x += point.lon
        sum_y += point.lat
    return GeoPoint(lon=sum_x / len(cluster), lat=sum_y / len(cluster))


def distribute_points(centroids, indices):
    clusters = [[] for _ in range(len(centroids))]
    for index in indices:
        point = kg.data[index]
        min_centroid = 0
        min_dist = None
        for idx, centroid in enumerate(centroids):
            dist = calc_dist(point, centroid)
            if min_dist is None or dist < min_dist:
                min_dist = dist
                min_centroid = idx
        clusters[min_centroid].append(point)

    return clusters


def calc_dist_sse(centroids, clusters):
    distances = 0
    for centroid, cluster in zip(centroids, clusters):
        for point in cluster:
            distances += dist_square(centroid, point)
    return distances
