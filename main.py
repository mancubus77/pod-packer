# Project libs
from lib.create_pod_list import CreatPodList
from lib.log_logger import logger
from lib.node import Node, NodeClass
from lib.node_list import Nodes
from lib.cvs_loader import csv_to_json
from lib.arg_parser import parse_args
from lib.result_printer import print_results

# Constants
MIN_WORKERS = 3
COMPUTE_CPU = 104
COMPUTE_MEM = 384000
ALLOCATION_PERCENT = 70
SCHEDULING = 1
FAULTSIMULATION = 2


def run_allocations(pods, mode=SCHEDULING):
    """
    Start pod allocation process
    :pods List of Pods
    :return: None
    """
    # Allocate nodes
    for _pod in pods:
        if (
            not (_node := node_list.find_node(_pod, exclude_node=None))
            and mode == SCHEDULING
        ):
            logger.warning("Can not find schedulable node. Adding new one")
            _node = Node(
                name=len(node_list),
                mem_total=COMPUTE_MEM,
                cpu_total=COMPUTE_CPU,
                allocation=ALLOCATION_PERCENT,
            )
            node_list.add_node(_node)
        elif mode == FAULTSIMULATION:
            logger.error("TEST FAILED")
        _node.add_pod(_pod)


if __name__ == "__main__":
    args = parse_args()
    node_list = Nodes()
    apps = sorted(csv_to_json(args.filename), key=lambda i: i["affinity"], reverse=True)
    pods_list = CreatPodList.add_pods(apps)

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
    # Runa allocations
    run_allocations(pods_list)
    # Run Fault simulation
    # test_fault(node_list)
    # Print Results
    print_results(args, node_list)
