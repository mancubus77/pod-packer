# The logic borrowed from here: https://access.redhat.com/solutions/5843241
# and here: https://github.com/openshift/machine-config-operator/blob/02b4d9cb446ce58dc9e895e617917bdc653ca50b/templates/common/_base/files/kubelet-auto-sizing.yaml#L11


def kublet_reserve_mem(total_memory: int) -> int:
    """Dynamically calculate memory for kubelet

    Args:
        total_memory (int): total node memory in MB

    Returns:
        int: required kubelet memory in MB
    """
    total_memory = round(total_memory / 1000)
    recommended_systemreserved_memory = 0

    if total_memory <= 1:
        return 256

    # 25% of the first 4GB of memory
    if total_memory <= 4:
        recommended_systemreserved_memory += total_memory * 0.25
        total_memory = 0
    else:
        recommended_systemreserved_memory = 1
        total_memory -= 4

    # 20% of the next 4GB of memory (up to 8GB)
    if total_memory <= 4:
        recommended_systemreserved_memory += total_memory * 0.20
        total_memory = 0
    else:
        recommended_systemreserved_memory += 0.8
        total_memory -= 4

    # 10% of the next 8GB of memory (up to 16GB)
    if total_memory <= 8:
        recommended_systemreserved_memory += total_memory * 0.1
        total_memory = 0
    else:
        recommended_systemreserved_memory += 0.8
        total_memory -= 8

    # then # 6% of the next 112GB of memory (up to 128GB)
    if total_memory <= 112:
        recommended_systemreserved_memory += total_memory * 0.06
        total_memory = 0
    else:
        recommended_systemreserved_memory += 6.72
        total_memory -= 112

    # then # 2% of any memory above 128GB
    if total_memory >= 0:
        recommended_systemreserved_memory += total_memory * 0.02

    return round(recommended_systemreserved_memory) * 1000


def kublet_reserve_cpu(total_cpu: int) -> int:
    """Dynamically calculate CPU for kubelet

    Args:
        total_cpu (int): total node CPU

    Returns:
        int:  required kubelet CPUs
    """
    recommended_systemreserved_cpu = 0

    # 6% of the first core
    if total_cpu <= 1:
        recommended_systemreserved_cpu = total_cpu * 0.06
        total_cpu = 0
    else:
        recommended_systemreserved_cpu = 0.06
        total_cpu -= 1

    # 1% of the next core (up to 2 cores)
    if total_cpu <= 1:
        recommended_systemreserved_cpu += total_cpu * 0.01
        total_cpu = 0
    else:
        recommended_systemreserved_cpu += 0.01
        total_cpu -= 1

    # 0.5% of the next 2 cores (up to 4 cores)
    if total_cpu <= 2:
        recommended_systemreserved_cpu += total_cpu * 0.005
        total_cpu = 0
    else:
        recommended_systemreserved_cpu += 0.01
        total_cpu -= 2

    # 0.25% of any cores above 4 cores
    if total_cpu >= 0:
        recommended_systemreserved_cpu += total_cpu * 0.0025

    if round(recommended_systemreserved_cpu) == 0:
        return 1
    else:
        return round(recommended_systemreserved_cpu)
