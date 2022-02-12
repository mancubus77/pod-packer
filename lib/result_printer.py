from lib.bftable import BTable


def print_results(args, node_list, summary_only=None):
    """
    Print text table
    :param args:
    :param node_list:
    :param summary_only:
    :return:
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
    if args.csv and not summary_only:
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
    if summary_only:
        print(table)
        return
    if args.detail and not args.csv:
        print(pod_table)
        print(f"{table}")
    elif args.detail and args.csv:
        print(f"\n".join(summary_csv))
    print(f"SUMMARY\n{summary_table}")
