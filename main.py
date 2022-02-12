import sys
import copy

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


def run_allocations(pods, mode=SCHEDULING, fault_simulation=None, excluded_node=None):
    """
    Pod allocation
    :param pods: pods to be allocated
    :param mode: Mode for allocation: SCHEDULING - normal allocation; FAULTSIMULATION - simulates one node failure and rebalance it's pods on other nodes
    :param fault_simulation: node_list for simulation
    :param excluded_node: Exclude failed node from nodes for scheduling
    :return: no
    """
    # Allocate nodes
    for _pod in pods:
        if mode == SCHEDULING:
            if not (_node := node_list.find_node(_pod)):
                logger.warning("Can not find schedulable node. Adding new one")
                _node = Node(
                    name=len(node_list),
                    mem_total=COMPUTE_MEM,
                    cpu_total=COMPUTE_CPU,
                    allocation=ALLOCATION_PERCENT,
                )
                node_list.add_node(_node)
            else:
                _node.add_pod(_pod)
        elif mode == FAULTSIMULATION:
            if not (
                _node := fault_simulation.find_node(_pod, exclude_node=excluded_node)
            ):
                logger.error(
                    f"FAILED: Can not evict {_pod.get('app')} from failed node {excluded_node.name}\n"
                    f"Reconsider ALLOCATION_PERCENT values, it's {ALLOCATION_PERCENT}% now\n"
                    f"Allocated nodes: {len(node_list.node_list)}"
                )
                print_results(args, node_list, summary_only=True)
                sys.exit(255)
            else:
                _node.add_pod(_pod)


def run_simulation():
    """
    Simulation of failed node
    ATM only one node is supported
    :return: none
    """
    print(f"Simulating node failure. Anit-Affinity violations will be ignored")
    for failed_node in node_list.node_list:
        fault_simulation = copy.deepcopy(node_list)
        logger.info(f"Running Simulation for {failed_node.name}")
        run_allocations(
            failed_node.pods,
            fault_simulation=fault_simulation,
            mode=FAULTSIMULATION,
            excluded_node=failed_node,
        )


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
    run_simulation()
    # Print Results
    print_results(args, node_list)
