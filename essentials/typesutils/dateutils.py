import re
from datetime import date, datetime, time
from typing import Any, Callable, Type, TypeVar, Union, overload

from essentials.exceptions import EmptyArgumentException

__all__ = ["parse", "parse_datetime", "parse_date", "parse_time"]

T = TypeVar("T")
time_rx = re.compile("(\\d{2})\\D(\\d{1,2})(?:\\D(\\d{1,2}))?")
date_rx = re.compile("(\\d{4})\\D(\\d{1,2})\\D(\\d{1,2})?")
datetime_rx = re.compile(
    "(\\d{4})\\D(\\d{1,2})\\D(\\d{1,2})(?:\\D{1}(\\d{1,2})"
    "\\D(\\d{1,2})(?:\\D(\\d{1,2}))?(?:\\D(\\d+))?)?"
)


def parse_with_rx(value: Any, rx: re.Pattern, desired_type: Callable[..., T]) -> T:
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


def parse_time(value: Any) -> time:
    return parse_with_rx(value, time_rx, time)


def parse_date(value: Any) -> date:
    return parse_with_rx(value, date_rx, date)


def parse_datetime(value: Any) -> datetime:
    return parse_with_rx(value, datetime_rx, datetime)


@overload
def parse(value: Any, desired_type: Type[datetime]) -> datetime: ...  # noqa:E704


@overload
def parse(value: Any, desired_type: Type[date]) -> date: ...  # noqa:E704


@overload
def parse(value: Any, desired_type: Type[time]) -> time: ...  # noqa:E704


def parse(
    value: Any, desired_type: Union[Type[datetime], Type[date], Type[time]]
) -> Union[datetime, date, time]:
    if desired_type == datetime:
        return parse_datetime(value)
    if desired_type == date:
        return parse_date(value)
    if desired_type == time:
        return parse_time(value)
    raise ValueError("Unsupported desired_type")
