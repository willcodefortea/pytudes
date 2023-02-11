from rover import execute
import pytest


@pytest.mark.parametrize(
    "input,obsticles,expected",
    [
        ("MMRMMLM", [], "2:3:N"),
        ("MMMMMMMMMM", [], "0:0:N"),
        ("MMMM", [3j], "O:0:2:N"),
    ],
)
def test_execute(input, obsticles, expected):
    assert execute(input, (10, 10), obsticles) == expected
