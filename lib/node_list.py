from typing import TypeVar, Generic

# project type
from lib.log_logger import logger
from lib.node import NodeClass

NodeListClass = TypeVar("NodeListClass")


class Nodes(Generic[NodeListClass]):
    """
    NODES class to store nodes
    """

    def __init__(self):
        self.node_list = []

    def add_node(self, node: object) -> int:
        """
        Add node to list
        :param node:
        :return: number of nodes in pool after adding
        """
        self.node_list.append(node)
        return len(self.node_list)

    @staticmethod
    def is_affinity_full(pod: dict, node: NodeClass) -> bool:
        """
        Check affinity rules on a node
        :param pod: Pod Specs
        :param node: Node object
        :return: True - Pod has a copy on node; False - all good
        """
        if not pod.get("affinity") and pod.get("affinity") == 0:
            return False
        entries = len([v for v in node.pods if v.get("app") == pod["app"]])
        if entries >= pod["max_per_node"]:
            logger.info(f"Pod {pod['app']} has {entries} copies in {node.name}")
            return True
        else:
            return False

    def is_node_schedulable(self, node: NodeClass, pod: dict, failure=None) -> bool:
        """
        Check if pod can be schedulable on a node and doesn't have
        memory constrains or affinity rules violation
        :param node: Node object
        :param pod: Pod specs
        :param failure: Simulate failure
        :return: True - Node is schedulable, False - node is not schdulable take next
        """
        if not failure and self.is_affinity_full(pod, node):
            logger.warning(f"{node.name} affinity violation for {pod['app']}")
            return False
        elif (
            node.cpu_used + pod["cpu"] > node.cpu_available
            or node.mem_used + pod["mem"] > node.mem_available
        ) and not failure:
            logger.warning(
                f"Node {node.name} is full: CPU: {node.cpu_used + pod['cpu'] > node.cpu_available} "
                f"MEM: {node.mem_used + pod['mem'] > node.mem_available} "
                f"{node.mem_used + pod['mem']} : {node.mem_available}"
            )
            return False
        elif (
            node.cpu_used + pod["cpu"] > node.cpu_total
            or node.mem_used + pod["mem"] > node.mem_total
        ) and failure:
            logger.warning(
                f"Node {node.name} is full: CPU: {node.cpu_used + pod['cpu'] > node.cpu_available} "
                f"MEM: {node.mem_used + pod['mem'] > node.mem_available} "
                f"{node.mem_used + pod['mem']} : {node.mem_available}"
            )
            return False
        else:
            return True

    def find_node(self, pod: dict, exclude_node=None):
        """
        Find available node what can accommodate  POD
        :param pod: pod specs
        :param exclude_node: Node excluded from scheduling
        :return: Node object
        """
        s = self.node_list
        s.sort(key=lambda x: x.pods_total)
        for _node in s:
            if _node == exclude_node:
                logger.info(f"Excluding node {_node.name}")
                continue
            if self.is_node_schedulable(_node, pod, failure=exclude_node):
                return _node
            else:
                continue
        return False

    def __len__(self):
        """
        Return nodes in object
        :return:
        """
        return len(self.node_list)
