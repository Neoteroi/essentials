import re
from datetime import date, datetime, time

from essentials.exceptions import EmptyArgumentException

__all__ = ["parse", "parse_datetime", "parse_date", "parse_time"]

time_rx = re.compile("(\\d{2})\\D(\\d{1,2})(?:\\D(\\d{1,2}))?")
date_rx = re.compile("(\\d{4})\\D(\\d{1,2})\\D(\\d{1,2})?")
datetime_rx = re.compile(
    "(\\d{4})\\D(\\d{1,2})\\D(\\d{1,2})(?:\\D{1}(\\d{1,2})"
    "\\D(\\d{1,2})(?:\\D(\\d{1,2}))?(?:\\D(\\d+))?)?"
)


def parse_with_rx(value, rx, desired_type):
    if not value:
        raise EmptyArgumentException("value")
    value = str(value)
    m = rx.match(value)
    if not m:
        raise ValueError(
            f"Value '{value}' cannot be parsed " f"as a {desired_type.__name__}."
        )
    args = [int(x) if x is not None else 0 for x in m.groups()]
    return desired_type(*args)


def parse_time(value):
    return parse_with_rx(value, time_rx, time)


def parse_date(value):
    return parse_with_rx(value, date_rx, date)


def parse_datetime(value):
    return parse_with_rx(value, datetime_rx, datetime)


def parse(value, desired_type):
    if desired_type == datetime:
        return parse_datetime(value)
    if desired_type == date:
        return parse_date(value)
    if desired_type == time:
        return parse_time(value)
    raise ValueError("Unsupported desired_type")
