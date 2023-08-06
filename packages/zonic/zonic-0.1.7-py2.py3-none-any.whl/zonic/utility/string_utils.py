import typing


class StringTemplate:
    """
    Encapsulating colourised string messages that can be written to
    standard out, when inspected the instance the colours are
    substituted into the string, for use in colourised output.

    :
    """

    def __init__(
        self,
        message: str,
        colour_options: typing.Optional[typing.Tuple[str, ...]] = None,
    ) -> None:
        self.message = message
        self.colour_options = colour_options

    def __repr__(self) -> str:
        return (
            self.message
            if not self.colour_options
            else self.message.format(*self.colour_options)
        )
