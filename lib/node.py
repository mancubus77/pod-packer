from typing import TypeVar, Generic
from lib.log_logger import logger

NodeClass = TypeVar("NodeClass")

KUBELET_MEMORY_RESERVE = 14000
KUBELET_VCPU_RESERVE = 7


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
        # Kubelet and OCP Memory Reserves: 13550
        # Kubelet and OCP CPU Reserves: 7000
        self.mem_total = mem_total - KUBELET_MEMORY_RESERVE
        self.cpu_total = cpu_total - KUBELET_VCPU_RESERVE
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
