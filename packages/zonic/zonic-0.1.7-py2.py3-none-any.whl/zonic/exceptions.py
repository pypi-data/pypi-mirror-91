class PortRangeValueError(ValueError):
    def __init__(self, value: str) -> None:
        super().__init__(self)
        self.message = (
            f"Invalid value specified for --port-range: `{value}`, "
            f"correct usage is: `--port-range | -pr 20-8080`"
        )
