from typing import Iterable


class Configuration:
    def __init__(
        self,
        target: str,
        verbose: bool,
        quick: bool,
        irregular: bool,
        thread_count: int,
        port_range: Iterable[int],
        csv_output: bool,
    ) -> None:
        self.target = target
        self.verbose = verbose
        self.quick = quick
        self.irregular = irregular
        self.thread_count = thread_count
        self.port_range = port_range
        self.csv_output = csv_output

    def __repr__(self) -> str:
        return (
            f"Configuration(target={self.target}, "
            f"verbose={self.verbose}, "
            f"quick={self.quick}, "
            f"irregular={self.irregular}, "
            f"thread_count={self.thread_count}, "
            f"port_range={self.port_range}, "
            f"csv_output={self.csv_output})"
        )
