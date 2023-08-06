import abc
import typing

from zonic.utility.string_utils import StringTemplate


class Attackable(abc.ABC):
    @abc.abstractmethod
    def attack(
        self, port_range: typing.Iterable[int]
    ) -> typing.Optional[typing.Iterable[int]]:
        """
        Begin attacking ports in the port range
        """
        ...


class Scanable(abc.ABC):
    @abc.abstractmethod
    def scan(self, port: int) -> typing.Tuple[int, bool]:
        """
        Perform a port scan against a particular port.
        :param port: The port (integer) to perform the scan against
        :return: A tuple of (port_number, boolean to indicate if port was considered `open`
        """
        ...


class Writable(abc.ABC):
    @abc.abstractmethod
    def write(self, template: StringTemplate, flush: bool = True) -> None:
        """
        Write messages to standard out
        :param template: StringTemplate instance to be written to stdout
        :param flush: A boolean flag to indicate if a flush should be performed after
        """
        ...
