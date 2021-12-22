from math import floor


class CreatPodList(object):
    @staticmethod
    def add_pods(pods=list) -> list:
        """
        Pods generator
        :param pods: list of pods
        :return: Pod Spec
        """
        for pod in pods:
            for values in map(
                lambda x: {
                    "app": pod["app"],
                    "mem": int(pod["mem"]),
                    "cpu": int(pod["cpu"]) / 1000,
                    "affinity": int(pod["affinity"]),
                    "max_per_node": floor(int(pod["count"]) / int(pod["affinity"]))
                    if pod["affinity"] != ""
                    else None,
                },
                range(int(pod["count"])),
            ):
                yield values
