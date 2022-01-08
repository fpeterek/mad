from enum import Enum
from typing import Any


class Message:
    class Type(Enum):
        CLUSTERIZE = 1
        CENTROIDS = 2
        STOP = 3

    def __init__(self, msg_type: Type, data: Any | None = None, order: int = -1):
        self.type = msg_type
        self.data = data
        self.order = order
