from typing import TypeVar, Generic
from lib.log_logger import logger

NodeClass = TypeVar("NodeClass")


class Node(Generic[NodeClass]):
    """
    Node Class to store pods
    """

    def __init__(self, name: int, mem_total: int, cpu_total: int, allocation: int):
        self.mem_total = mem_total
        self.cpu_total = cpu_total
        self.allocation = allocation
        self.mem_available = mem_total * (allocation / 100)
        self.cpu_available = cpu_total * (allocation / 100)
        self.mem_used = 0
        self.cpu_used = 0
        self.pods = []
        self.pods_total = len(self.pods)
        self.name = f"compute-{str(name)}"
        self.status = int
        logger.info(f"Creating new node compute-{str(name)}")

    def add_pod(self, pod: dict) -> int:
        """
        Add pod to node
        :param pod: pod spec
        :return: I
        """
        self.mem_used += pod["mem"]
        self.cpu_used += pod["cpu"]
        self.pods.append(pod)
        self.pods_total = len(self.pods)
        return len(self.pods)
