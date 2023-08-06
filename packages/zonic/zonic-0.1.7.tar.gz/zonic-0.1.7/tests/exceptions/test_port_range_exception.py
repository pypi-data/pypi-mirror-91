import subprocess

import pytest
from assertpy import assert_that

from zonic.exceptions import PortRangeValueError


@pytest.mark.parametrize(
    "port_range, expected",
    [("10-100s", 1), ("", 1), ("fail", 1), ("20 8080", 1), ("20-8080", 0)],
)
def test_exit_codes_for_port_range(port_range, expected) -> None:
    exit_code = 0
    try:
        subprocess.check_output(["zonic", "-t", "localhost", "-pr", port_range])
    except subprocess.CalledProcessError as err:
        exit_code = err.returncode
    assert_that(exit_code).is_equal_to(expected)


def test_port_range_exc_message() -> None:
    expected = (
        "Invalid value specified for --port-range: `fail=true`,"
        " correct usage is: `--port-range | -pr 20-8080`"
    )
    with pytest.raises(PortRangeValueError) as err:
        raise PortRangeValueError(value="fail=true")
    assert_that(err.value.message).is_equal_to(expected)  # type: ignore
