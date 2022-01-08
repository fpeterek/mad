import multiprocessing as mp
from typing import Optional


data: list | None = None
in_queue: Optional[mp.Queue] = None
out_queue: Optional[mp.Queue] = None
