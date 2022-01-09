from data.geo_point import GeoPoint


Cluster = list[GeoPoint]


def in_cluster_distance(point: GeoPoint, cluster: Cluster) -> float:
    dist_sum = 0
    for p in cluster:
        if point is p:
            continue
        dist_sum = p.distance(point)
    return 1 if not len(cluster) - 1 else dist_sum / (len(cluster) - 1)


def nearest_cluster_dist(point: GeoPoint, clusters: list[Cluster], exclude: Cluster) -> float:
    min_dist = None

    for cluster in clusters:
        dist_sum = 0
        if cluster == exclude:
            continue
        for p in cluster:
            dist_sum += p.distance(point)
        dist_avg = dist_sum / len(cluster)
        if min_dist is None or dist_avg < min_dist:
            min_dist = dist_avg

    return min_dist


def silhouette_index(clusters: list[Cluster]) -> float:
    index_sum = 0
    points = 0
    for cluster in clusters:
        for point in cluster:
            points += 1
            a = in_cluster_distance(point, cluster)
            b = nearest_cluster_dist(point, clusters, exclude=cluster)
            index_sum += (b - a) / max(a, b)

    return index_sum / points

