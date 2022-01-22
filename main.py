import logging

from lib.create_pod_list import CreatPodList
from argparse import ArgumentParser

# Project libs
from lib.log_logger import logger
from lib.node import Node, NodeClass
from lib.node_list import Nodes
from lib.cvs_loader import csv_to_json
from lib.bftable import BTable

# Constants
MIN_WORKERS = 3
COMPUTE_CPU = 104
COMPUTE_MEM = 384000
ALLOCATION_PERCENT = 70


def parse_args():
    parser = ArgumentParser(description="Read CSV form given path.")
    parser.add_argument(
        "-i",
        "--input",
        dest="filename",
        required=True,
        help="input file",
        metavar="FILE",
    )
    parser.add_argument(
        "-d",
        "--detail",
        dest="detail",
        required=False,
        action="store_true",
        help="Detailed view of pods breakdown",
    )
    parser.add_argument(
        "--csv",
        dest="csv",
        required=False,
        action="store_true",
        help="csv output, needs to be used with -d/--detail",
    )

    return parser.parse_args()


def run_allocations():
    """
    Start pod allocation process
    :return: None
    """
    # Allocate nodes
    for _pod in CreatPodList.add_pods(apps):
        if not (_node := node_list.find_node(_pod)):
            logger.warning("Can not find schedulable node. Adding new one")
            _node = Node(
                name=len(node_list),
                mem_total=COMPUTE_MEM,
                cpu_total=COMPUTE_CPU,
                allocation=ALLOCATION_PERCENT,
            )
            node_list.add_node(_node)
        _node.add_pod(_pod)


def print_results():
    table = BTable()
    pod_table = BTable()
    table.create_heading(["node",
                          "pod count",
                          "cpu",
                          "cpu,%",
                          "mem, GB",
                          "mem,%",
                          ])
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
        if args.detail:
            for pod in node.pods:
                if not pod_table.is_headings():
                    pod_table.create_heading(["node"] + [k for k in pod.keys()])
                pod_table.append_row([node.name] + [v for v in pod.values()])
                if args.csv:
                    print(",".join([node.name] + [str(v) for v in pod.values()]))
    print(pod_table) if (args.detail and not args.csv) else None
    print(table)


if __name__ == "__main__":
    args = parse_args()
    node_list = Nodes()
    apps = csv_to_json(args.filename)
    logger.info(f"Starting allocation, there are {len(apps)} apps to be allocated")
    for _ in range(MIN_WORKERS):
        node_list.add_node(
            node=Node(
                name=len(node_list),
                mem_total=COMPUTE_MEM,
                cpu_total=COMPUTE_CPU,
                allocation=ALLOCATION_PERCENT,
            )
        )
    run_allocations()
    # Print Results
    print_results()
