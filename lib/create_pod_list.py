from math import floor

#TODO: Track odd pod counts or anti-affinity and use CEILING instead of FLOOR
class CreatPodList(object):
    @staticmethod
    def get_antiaffinity(anti_affinity: int) -> int:
        """
        Update Anti Affinity if it's blank or none
        :param anti_affinity: anti affinity int (input)
        :return: anti affinity int (output)
        """
        if anti_affinity == 0:
            return 1
        else:
            return anti_affinity

    @staticmethod
    def add_pods(pods: list) -> list:
        """
        Pods generator
        :param pods: list of pods
        :return: Pod Spec
        """
        for pod in pods:
            for values in map(
                lambda x: {
                    "app": pod["app"]
                    if "platform" not in pod
                    else f"{pod['platform']}/{pod['app']}",
                    "mem": int(pod["mem"]),
                    "cpu": int(pod["cpu"]) / 1000,
                    "affinity": CreatPodList.get_antiaffinity(int(pod["affinity"])),
                    "max_per_node": floor(
                        int(pod["count"])
                        / CreatPodList.get_antiaffinity(int(pod["affinity"]))
                    )
                    if pod["affinity"] != ""
                    else None,
                },
                range(int(pod["count"])),
            ):
                yield values
