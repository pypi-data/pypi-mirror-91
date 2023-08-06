import abc
import logging

__all__ = ["multihash", "Comparable"]

log = logging.getLogger(__name__)


def multihash(*args):
    """Multi-argument order-sensitive hash.

    Args:
        *args: Objects to hash.

    Returns:
        int: Hash.
    """
    return hash(args)


class Comparable:
    """A mixin that makes instances of the class comparable.

    Requires the subclass to just implement `__le__`.
    """

    __metaclass__ = abc.ABCMeta

    def __eq__(self, other):
        return self <= other <= self

    def __ne__(self, other):
        return not self == other

    @abc.abstractmethod
    def __le__(self, other):
        pass  # pragma: no cover

    def __lt__(self, other):
        return self <= other and self != other

    def __ge__(self, other):
        return other.__le__(self)

    def __gt__(self, other):
        return self >= other and self != other

    def is_comparable(self, other):
        """Check whether this object is comparable with another one.

        Args:
            other (:class:`.util.Comparable`): Object to check comparability
                with.

        Returns:
            bool: `True` if the object is comparable with `other` and `False`
                otherwise.
        """
        return self < other or self == other or self > other

