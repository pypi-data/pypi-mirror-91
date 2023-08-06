"""Console script for zonic."""
import argparse
import socket
import sys

import colorama

from .configuration import Configuration
from .impl import Attacker
from .impl import Scanner
from .impl import Writer
from .instance import ZonicInstance
from .utility.argparsing import RangeAction


def parse_sysargv() -> argparse.Namespace:
    """
    Parses sys.argv via the argparse module.
    store_true | store_false are implicit in their values, however we are explicit here.
    :return: The argparse.Namespace instance from `parse_args()`
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--target",
        action="store",
        required=True,
        dest="target",
        type=socket.gethostbyname,
        metavar="localhost",
        help="Target host used for port inspection.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increase verbosity, zonic supports a simple ON|OFF verbosity level over count(-vvv) etc.",
        dest="verbose",
        default=False,
    )
    parser.add_argument(
        "-q",
        "--quick",
        action="store_true",
        help="Scan the range of common ports, disregarding --port-range.",
        dest="quick",
    )
    parser.add_argument(
        "-i",
        "--irregular",
        action="store_true",
        help="Ports are randomly scanned (even when threading the workload) to avoid sequential execution "
        "Some systems can spot the pattern originating and activate blocking mechanism quicker.",
        dest="irregular",
    )
    parser.add_argument(
        "-tc",
        "--thread-count",
        action="store",
        type=int,
        default=1_000,
        metavar="2000",
        help="Number of threads to use for scanning, scanning is IO bound and substancial performance"
        "gains can be had (at the price of load on the target host)",
        dest="thread_count",
    )
    parser.add_argument(
        "-pr",
        "--port-range",
        action=RangeAction,
        default=range(65536),
        metavar="22-8080",
        help="Specifying a port range",
        dest="port_range",
    )
    parser.add_argument(
        "-csv",
        "--csv-output",
        action="store_true",
        default=False,
        help="Write the vulnerable ports to a csv file in the current working directory.",
        dest="csv_output",
    )
    return parser.parse_args()


def main():
    colorama.init()
    namespace = parse_sysargv()
    config = Configuration(**vars(namespace))
    scanner = Scanner(config)
    attacker = Attacker()
    zonic = ZonicInstance(
        config=config, scannable=scanner, attackable=attacker, writable=Writer()
    )
    zonic.display_configuration()
    zonic.attack()


def init() -> None:
    # unit testable
    if __name__ == "__main__":
        sys.exit(main())  # pragma: no cover


init()
