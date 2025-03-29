from datetime import time
from enum import Enum


class TimePrecision(Enum):
    HOUR = 1
    MINUTE = 2
    SECOND = 3
    MICROSECOND = 4


def time_to_seconds(value: time) -> int:
    """
    Gets the total seconds from a time object,
    discarding its microseconds information.
    """
    return value.hour * 60 * 60 + value.minute * 60 + value.second


def time_from_seconds(s: int) -> time:
    """Creates a new time object from seconds."""
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return time(int(h), int(m), int(s))


def time_to_microseconds(value: time) -> float:
    """Gets the total microseconds from a time object."""
    b = 1e6
    return (
        value.hour * 60 * 60 * b
        + value.minute * 60 * b
        + value.second * b
        + value.microsecond
    )


def time_from_microseconds(a: int) -> time:
    """Creates a new time object from microseconds."""
    s, x = divmod(a, 1000000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return time(int(h), int(m), int(s), int(x))


def get_time_precision(*args) -> TimePrecision:
    """Returns the minimum TimePrecision that can be used to represent a time."""
    if any(o.microsecond > 0 for o in args):
        return TimePrecision.MICROSECOND

    if any(o.second > 0 for o in args):
        return TimePrecision.SECOND

    if any(o.minute > 0 for o in args):
        return TimePrecision.MINUTE

    return TimePrecision.HOUR
