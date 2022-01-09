import math
import multiprocessing as mp

import kmeans.globals as kg
from kmeans.kmeans_core import calc_centroid, distribute_points
from kmeans.message import Message
from data.geo_point import GeoPoint


def calc_centroids_in_serial(clusters) -> list[GeoPoint]:
    centroids = [calc_centroid(c) for c in clusters]
    return [centroid for centroid in centroids if centroid]


def calc_centroids_in_parallel(clusters):
    for idx, cluster in enumerate(clusters):
        kg.in_queue.put(Message(msg_type=Message.Type.CENTROIDS, data=cluster, order=idx))
    centroids = [kg.out_queue.get() for _ in range(len(clusters))]
    centroids = [centroid for centroid in centroids if centroid is not None]
    centroids.sort(key=lambda msg: msg.order)
    return [msg.data for msg in centroids]


def calc_ranges(points, processes) -> list[range]:
    splits = []
    split_size = math.ceil(len(points) / processes)
    for i in range(processes):
        begin = i * split_size
        end = min((i+1) * split_size, len(points))
        splits.append(range(begin, end))
        if end >= len(points):
            break

    return splits


def distribute_in_serial(centroids, points, _):
    return distribute_points(centroids, range(len(points)))


def merge_results(messages: list[Message]) -> list[list]:
    res = []
    for msg in messages:
        for idx, cluster in enumerate(msg.data):
            if len(res) <= idx:
                res.append([])
            res[idx] += cluster
    return res


def distribute_in_parallel(centroids, points, processes):
    splits = calc_ranges(points, processes)

    for split in splits:
        kg.in_queue.put(Message(msg_type=Message.Type.CLUSTERIZE, data=(centroids, split)))
    res = [kg.out_queue.get() for _ in range(len(splits))]

    return merge_results(res)


def distribute_message(msg: Message):
    centroids, split = msg.data
    clusters = distribute_points(centroids, split)

    if kg.out_queue is not None:
        kg.out_queue.put(Message(msg_type=Message.Type.CLUSTERIZE, data=clusters))


def centroid_message(msg: Message):
    cluster = msg.data
    centroid = calc_centroid(cluster)

    if kg.out_queue is not None:
        kg.out_queue.put(Message(msg_type=Message.Type.CENTROIDS, data=centroid, order=msg.order))


def run_process():
    fns = {Message.Type.CLUSTERIZE: distribute_message, Message.Type.CENTROIDS: centroid_message}
    while True:
        msg: Message = kg.in_queue.get()
        if msg.type in fns:
            fns[msg.type](msg)
        if msg.type == Message.Type.STOP:
            return


def create_processes(num_processes):
    if num_processes < 2:
        return []
    processes = [mp.Process(target=run_process) for _ in range(num_processes)]
    for p in processes:
        p.start()
    return processes
