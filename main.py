import sys
import copy

# Project libs
from lib.create_pod_list import CreatPodList
from lib.log_logger import logger, level
from lib.node import Node
from lib.node_list import Nodes
from lib.cvs_loader import csv_to_json
from lib.arg_parser import parse_args
from lib.result_printer import print_results

# Config
from config import MIN_WORKERS, COMPUTE_CPU, COMPUTE_MEM, ALLOCATION_PERCENT

# CONSTANTS/FLAGS
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
            new_node = False
            if not (_node := node_list.find_node(_pod)):
                logger.warning("Can not find schedulable node. Adding new one")
                _node = Node(
                    name=len(node_list),
                    mem_total=COMPUTE_MEM,
                    cpu_total=COMPUTE_CPU,
                    allocation=ALLOCATION_PERCENT,
                )
                node_list.add_node(_node)
                new_node = True
            if new_node and (
                _node.cpu_available < _pod["cpu"] or _node.mem_available < _pod["mem"]
            ):
                if _node.cpu_available < _pod["cpu"]:
                    logger.error(
                        f"FAILED: Can not allocate pod {_pod['app']}, on node {_node.name} "
                        f"as pod CPU requirements higher than vCPU on server "
                        f"Node CPU>: {_node.cpu_available} < {_pod['cpu']} "
                    )
                    sys.exit(255)
                elif _node.mem_available < _pod["mem"]:
                    logger.error(
                        f"FAILED: Can not allocate pod {_pod['app']}, on node {_node.name} "
                        f"as pod Memory requirements higher than physical memory. "
                        f"Mem: {_node.mem_available} < {_pod['mem']}"
                    )
                    sys.exit(255)

                print_results(args, node_list, summary_only=True)
                sys.exit(255)
            _node.add_pod(_pod)
        elif mode == FAULTSIMULATION:
            if not (_node := node_list.find_node(_pod, exclude_node=excluded_node)):
                logger.error(
                    f"FAILED: Can not evict {_pod.get('app')} from failed node {excluded_node.name}\n"
                    f"Reconsider ALLOCATION_PERCENT values, it's {ALLOCATION_PERCENT}% now\n"
                    f"Allocated nodes: {len(node_list.node_list)}"
                )
                print_results(args, node_list, summary_only=True)
                sys.exit(255)
            # elif _node == excluded_node:
            #     continue
            else:
                # When pod can not be scheduled, because it's already has a copy
                _node.add_pod(_pod)


def run_simulation():
    """
    Simulation of failed node
    ATM only one node is supported
    :return: none
    """
    global node_list
    print("Simulating node failure. Anti-Affinity violations will be ignored")
    for failed_node in copy.deepcopy(node_list).node_list:
        fault_simulation_copy = copy.deepcopy(node_list)
        logger.info(f"Running Simulation for {failed_node.name}")
        for i, o in enumerate(node_list.node_list):
            if o.name == failed_node.name:
                del node_list.node_list[i]
                break
        run_allocations(
            failed_node.pods,
            mode=FAULTSIMULATION,
            excluded_node=failed_node.reset_allocation(),
        )
        print(f"Result of simulation for failed node {failed_node.name}")
        print_results(args, node_list, summary_only=True)
        node_list = copy.deepcopy(fault_simulation_copy)


if __name__ == "__main__":
    # Init classes
    args = parse_args()
    node_list = Nodes()
    # Init vars
    apps = sorted(csv_to_json(args.filename), key=lambda i: i["affinity"], reverse=True)
    pods_list = CreatPodList.add_pods(apps)

    logger.info(
        f"Starting allocation, there are {len(apps)} apps to be allocated. Log level {level}"
    )
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
    # Print Results
    print_results(args, node_list)
    # Run Fault simulation
    run_simulation()
