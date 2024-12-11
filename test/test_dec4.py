import pytest

from .. import dec4


def test_find_all_x():
    lines = ["XaX", "dXd", "ddX"]

    out = dec4.find_all_x(lines=lines)
    expected = [(0, 0), (0, 2), (1, 1), (2, 2)]
    assert out == expected


test_data = [
    (0, 0, 0, 1, True),
    (4, 4, 0, -1, True),
    (3, 4, -1, 0, True),
    (1, 1, 1, 1, False),
    (4, 4, 1, 1, False),
]


@pytest.mark.parametrize("x0,y0,xdir,ydir,expected", test_data)
def test_test_direction(x0: int, y0: int, xdir: int, ydir: int, expected: bool):
    match = "XMAS"
    lines = ["XMASS", "dMddA", "ddAdM", "dffSX", "dSAMX"]
    out = dec4.test_direction(
        lines=lines, match=match, x0=x0, y0=y0, xdir=xdir, ydir=ydir
    )
    assert out == expected
