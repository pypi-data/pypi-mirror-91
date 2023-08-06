import numpy as np

from plum.util import multihash, Comparable


def test_multihash():
    assert multihash(1, 2) == multihash(1, 2)
    assert multihash(2, 2) != multihash(1, 2)
    assert multihash(2, 1) != multihash(1, 2)


class Number(Comparable):
    def __init__(self, x):
        self.x = x

    def __le__(self, other):
        return self.x <= other.x


def test_comparable():
    assert Number(1) == Number(1)
    assert Number(1) != Number(2)
    assert Number(1) <= Number(2)
    assert Number(1) <= Number(1)
    assert Number(1) < Number(2)
    assert Number(2) >= Number(1)
    assert Number(2) >= Number(2)
    assert Number(2) > Number(1)
    assert Number(1).is_comparable(Number(2))
    assert not Number(1).is_comparable(Number(np.nan))


