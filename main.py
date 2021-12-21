from lib.create_pod_list import CreatPodList
from beautifultable import BeautifulTable
from argparse import ArgumentParser

# Project libs
from lib.log_logger import logger
from lib.node import Node, NodeClass
from lib.node_list import Nodes
from lib.cvs_loader import csv_to_json

# Constants
MIN_WORKERS = 3
COMPUTE_CPU = 104
COMPUTE_MEM = 384000
ALLOCATION_PERCENT = 70

if __name__ == "__main__":
    parser = ArgumentParser(description="Read CSV form given path.")
    parser.add_argument(
        "-i",
        "--input",
        dest="filename",
        required=True,
        help="input file",
        metavar="FILE",
    )
    args = parser.parse_args()
    print(args.filename)

    pods = csv_to_json(args.filename)
    logger.info(f"Starting allocation, there are {len(pods)} pods to be allocated")
    node_list = Nodes()
    for _ in range(MIN_WORKERS):
        node_list.add_node(
            node=Node(
                name=len(node_list),
                mem_total=COMPUTE_MEM,
                cpu_total=COMPUTE_CPU,
                allocation=ALLOCATION_PERCENT,
            )
        )
    # Allocate nodes
    for pod in CreatPodList.add_pods(pods):
        if not (node := node_list.find_node(pod)):
            logger.warning("Can not find schedulable node. Adding new one")
            node = Node(
                name=len(node_list),
                mem_total=COMPUTE_MEM,
                cpu_total=COMPUTE_CPU,
                allocation=ALLOCATION_PERCENT,
            )
            node_list.add_node(node)
        node.add_pod(pod)

    # Print Results
    table = BeautifulTable()
    table.column_headers = [
        "Node",
        "Pods",
        "CPU Used",
        "CPU Used, %",
        "MEM Used",
        "MEM Used, %",
    ]
    for node in node_list.node_list:
        table.append_row(
            [
                node.name,
                len(node.pods),
                node.cpu_used,
                (node.cpu_used / node.cpu_total) * 100,
                node.mem_used,
                (node.mem_used / node.mem_total) * 100,
            ]
        )
    print(table)
