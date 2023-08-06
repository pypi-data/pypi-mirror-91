import argparse
import typing

from zonic.exceptions import PortRangeValueError


class RangeAction(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: typing.Union[typing.Sequence[typing.Any], str, None],
        option_string: typing.Optional[str] = None,
    ):
        """
        This are only invoked if the respective argument we use it against is provided
        explicitly on the CLI; otherwise the default value is assumed.
        """
        assert isinstance(values, str)
        try:
            sep = "-"
            first, sep, second = values.partition(sep)
            setattr(namespace, self.dest, range(int(first), int(second)))
        except ValueError:
            raise PortRangeValueError(values) from None
