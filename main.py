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
    """
    Parse CLI arguments
    :return: parser object with arguments
    """
    parser = ArgumentParser(description="PODs scheduler simulator")
    parser.add_argument(
        "-i",
        "--input",
        dest="filename",
        required=True,
        help="path to CSV file with PODs ",
        metavar="FILE",
    )
    parser.add_argument(
        "-d",
        "--detail",
        dest="detail",
        required=False,
        action="store_true",
        help="Detailed view of pods breakdown per node",
    )
    parser.add_argument(
        "--csv",
        dest="csv",
        required=False,
        action="store_true",
        help="generates output in csv format, should be used with -d/--detail",
    )

    return parser.parse_args()


def run_allocations(pods):
    """
    Start pod allocation process
    :pods List of Pods
    :return: None
    """
    # Allocate nodes
    for _pod in pods:
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
    """
    Print neat table using BTable
    :return: Formatted Table with borders (string)
    """
    summary_csv = []
    table = BTable()
    pod_table = BTable()
    summary_table = BTable()
    summary_table.create_heading(["nodes", "pods", "cpu", "mem"])
    table.create_heading(
        ["node", "pod count", "cpu", "cpu,%", "mem, GB", "mem,%",]
    )
    # blah...
    if args.csv:
        print("node,app,mem,cpu,anti-affinity,max_per_node")
    for node in sorted(node_list.node_list, key=lambda i: i.name):
        if not args.csv:
            # Add row in formatted node table
            table.append_row(
                [
                    node.name,
                    len(node.pods),
                    node.cpu_used,
                    (node.cpu_used / node.cpu_total) * 100,
                    f"{node.mem_used:,}",
                    (node.mem_used / node.mem_total) * 100,
                ]
            )
        else:
            # Add row in CSV
            summary_csv.append(
                f"{node.name},"
                f"{len(node.pods)},"
                f"{node.cpu_used:.2f},"
                f"{(node.cpu_used / node.cpu_total) * 100:.2f},"
                f"{node.mem_used:.2f},"
                f"{(node.mem_used / node.mem_total) * 100:.2f}"
            )
        # Generate pods details per node
        if args.detail:
            for pod in node.pods:
                if not pod_table.is_headings():
                    pod_table.create_heading(["node"] + [k for k in pod.keys()])
                pod_table.append_row([node.name] + [v for v in pod.values()])
                if args.csv:
                    print(",".join([node.name] + [str(v) for v in pod.values()]))
    # Add row to summary table
    summary_table.append_row(
        [
            len(node_list.node_list),
            sum([len(i.pods) for i in node_list.node_list]),
            sum([i.cpu_used for i in node_list.node_list]),
            f"{sum([i.mem_used for i in node_list.node_list]):,}",
        ]
    )
    print(f"NODE BREAKDOWN")
    if args.detail and not args.csv:
        print(pod_table)
        print(f"{table}")
    elif args.detail and args.csv:
        print(f"\n".join(summary_csv))
    print(f"SUMMARY\n{summary_table}")


if __name__ == "__main__":
    args = parse_args()
    node_list = Nodes()
    apps = sorted(csv_to_json(args.filename), key=lambda i: i["affinity"], reverse=True)
    logger.info(f"Starting allocation, there are {len(apps)} apps to be allocated")
    # Create minimum workers pools
    for _ in range(MIN_WORKERS):
        node_list.add_node(
            node=Node(
                name=len(node_list),
                mem_total=COMPUTE_MEM,
                cpu_total=COMPUTE_CPU,
                allocation=ALLOCATION_PERCENT,
            )
        )
    run_allocations(CreatPodList.add_pods(apps))
    # Print Results
    print_results()
