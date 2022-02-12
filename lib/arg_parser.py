from argparse import ArgumentParser


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
