import logging

from .dispatcher import Dispatcher
from .function import promised_convert
from .parametric import type_of
from .type import as_type, TypeType

__all__ = [
    "convert",
    "add_conversion_method",
    "conversion_method",
    "add_promotion_rule",
    "promote",
]

log = logging.getLogger(__name__)

_dispatch = Dispatcher()


@_dispatch(object, TypeType)
def convert(obj, type_to):
    """Convert an object to a particular type.

    Args:
        obj (object): Object to convert.
        type_to (type): Type to convert to.

    Returns:
        object: `object_to_covert` converted to type of `obj_from_target`.
    """
    return _convert.invoke(type_of(obj), type_to)(obj, type_to)


# Deliver `convert`.
promised_convert.deliver(convert)


@_dispatch(object, object)
def _convert(obj, type_to):
    type_from = type_of(obj)
    type_to = as_type(type_to)
    if type_from <= type_to:
        return obj
    else:
        raise TypeError(f'Cannot convert a "{type_from}" to a "{type_to}".')


def add_conversion_method(type_from, type_to, f):
    """Add a conversion method to convert an object from one type to another.

    Args:
        type_from (type): Type to convert from.
        type_to (type): Type to convert to.
        f (function): Function that converts an object of type `type_from` to
            type `type_to`.
    """
    _convert.extend(type_from, type_to)(lambda obj, _: f(obj))


def conversion_method(type_from, type_to):
    """Decorator to add a conversion method to convert an object from one
    type to another.

    Args:
        type_from (type): Type to convert from.
        type_to (type): Type to convert to.
    """

    def add_method(f):
        add_conversion_method(type_from, type_to, f)

    return add_method


# Add some common conversion methods.
add_conversion_method(object, tuple, lambda x: (x,))
add_conversion_method(tuple, tuple, lambda x: x)
add_conversion_method(list, tuple, tuple)
add_conversion_method(object, list, lambda x: (x,))
add_conversion_method(list, list, lambda x: x)
add_conversion_method(tuple, list, list)
add_conversion_method(bytes, str, lambda x: x.decode("utf-8", "replace"))


@_dispatch(object, object)
def _promotion_rule(type1, type2):
    """Promotion rule.

    Args:
        type1 (ptype): First type to promote.
        type2 (ptype): Second type to promote.

    Returns:
        type: Type to convert to.
    """
    type1 = as_type(type1)
    type2 = as_type(type2)
    if type1 <= type2:
        return type2
    elif type2 <= type1:
        return type1
    else:
        raise TypeError(f'No promotion rule for "{type1}" and "{type2}".')


@_dispatch(object, object, object)
def add_promotion_rule(type1, type2, type_to):
    """Add a promotion rule.

    Args:
        type1 (type): First type to promote.
        type2 (type): Second type to promote.
        type_to (type): Type to convert to.
    """
    _promotion_rule.extend(type1, type2)(lambda t1, t2: type_to)
    if as_type(type1) != as_type(type2):
        _promotion_rule.extend(type2, type1)(lambda t1, t2: type_to)


@_dispatch(object, object, [object])
def promote(*objs):
    """Promote objects to a common type.

    Args:
        *objs (object): Objects to convert.

    Returns:
        tuple: `objs`, but all converted to a common type.
    """
    # Get the types of the objects.
    types = [type_of(obj) for obj in objs]

    # Find the common type.
    common_type = _promotion_rule.invoke(types[0], types[1])(types[0], types[1])
    for t in types[2:]:
        common_type = _promotion_rule.invoke(common_type, t)(common_type, t)

    # Convert objects and return.
    return tuple(convert(obj, common_type) for obj in objs)


@_dispatch(object)
def promote(obj):
    # Promote should always return a tuple to avoid edge cases.
    return (obj,)


@_dispatch()
def promote():
    return ()
