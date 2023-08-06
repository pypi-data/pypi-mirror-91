import typing

from zonic.abc.base_classes import Attackable


class Attacker(Attackable):
    def attack(
        self, port_range: typing.Iterable[int]
    ) -> typing.Optional[typing.Iterable[int]]:
        ...
