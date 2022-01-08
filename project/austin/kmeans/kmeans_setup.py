import multiprocessing as mp

import kmeans.globals as kg
from kmeans.message import Message


def setup(points, processes):
    kg.data = points
    if processes > 1:
        kg.in_queue = mp.Queue()
        kg.out_queue = mp.Queue()


def shutdown(processes):
    kg.data = None

    if processes is not None:
        for _ in processes:
            kg.in_queue.put(Message(msg_type=Message.Type.STOP))
        for p in processes:
            p.join()
            p.close()

    if kg.in_queue is not None:
        kg.in_queue.close()
        kg.in_queue = None
    if kg.out_queue is not None:
        kg.out_queue.close()
        kg.out_queue = None

