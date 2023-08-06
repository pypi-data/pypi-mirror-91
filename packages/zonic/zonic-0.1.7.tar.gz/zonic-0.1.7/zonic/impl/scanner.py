import typing

from zonic.abc.base_classes import Scanable
from zonic.configuration import Configuration


class Scanner(Scanable):
    def __init__(self, config: Configuration):
        self.config = config

    def scan(self, port: int) -> typing.Tuple[int, bool]:
        ...
