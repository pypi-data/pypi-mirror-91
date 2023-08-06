import pytest
from assertpy import assert_that

from zonic.utility.string_utils import StringTemplate


@pytest.mark.parametrize(
    "template, expected",
    [
        (StringTemplate(message="a{0}", colour_options=(" b",)), "a b"),
        (StringTemplate(message="foo", colour_options=None), "foo"),
    ],
)
def test_string_template(template, expected) -> None:
    assert_that(str(template)).is_equal_to(expected)
