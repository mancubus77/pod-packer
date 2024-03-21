from typing import TypeVar, Generic
from lib.log_logger import logger
from lib.dynamic_resources import kublet_reserve_mem, kublet_reserve_cpu

NodeClass = TypeVar("NodeClass")


class Node(Generic[NodeClass]):
    """
    Node Class to store pods
    """

    def __init__(self, name: int, mem_total: int, cpu_total: int, allocation: int):
        """
        Add new node with class creation
        :param name: Name of the node
        :param mem_total: Total memory
        :param cpu_total: Total vCPU
        :param allocation: Allowed CPU allocation
        """
        # Calculate dynamic kublet resource allocation
        self.mem_total = mem_total - kublet_reserve_mem(mem_total)
        self.cpu_total = cpu_total - kublet_reserve_cpu(cpu_total)
        self.allocation = allocation
        self.mem_available = self.mem_total * (allocation / 100)
        self.cpu_available = self.cpu_total * (allocation / 100)
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

    def reset_allocation(self):
        """
        Reset allocation for failover testing
        :return: none
        """
        self.mem_available = self.mem_total
        self.cpu_available = self.cpu_total
        return self

    def restore_allocation(self):
        """
        Restore allocation
        :return: none
        """
        self.mem_available = self.mem_total * (self.allocation / 100)
        self.cpu_available = self.cpu_total * (self.allocation / 100)
        return self
