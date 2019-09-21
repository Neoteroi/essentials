import pytest
from datetime import time
from essentials.typesutils.timeutils import (time_to_seconds,
                                         time_from_seconds,
                                         time_from_microseconds,
                                         time_to_microseconds,
                                         get_time_precision,
                                         TimePrecision)


@pytest.mark.parametrize('value,expected_seconds', [
    [time(0, 1, 0), 60],
    [time(0, 1, 0, 200), 60],
    [time(0, 5, 0), 60 * 5],
    [time(0, 5, 20), (60 * 5) + 20],
    [time(2, 5, 20), (60 * 60 * 2) + (60 * 5) + 20],
])
def test_time_to_seconds(value, expected_seconds):
    assert time_to_seconds(value) == expected_seconds


@pytest.mark.parametrize('expected_time,seconds', [
    [time(0, 1, 0), 60],
    [time(0, 5, 0), 60 * 5],
    [time(0, 5, 20), (60 * 5) + 20],
    [time(2, 5, 20), (60 * 60 * 2) + (60 * 5) + 20],
])
def test_time_from_seconds(seconds, expected_time):
    assert time_from_seconds(seconds) == expected_time


@pytest.mark.parametrize('expected_time,microseconds', [
    [time(0, 1, 0, 20), 60 * 1e6 + 20],
    [time(0, 5, 0, 333), 60 * 5 * 1e6 + 333],
])
def test_time_from_microseconds(microseconds, expected_time):
    assert time_from_microseconds(microseconds) == expected_time


@pytest.mark.parametrize('value,expected_microseconds', [
    [time(0, 1, 0, 20), 60 * 1e6 + 20],
    [time(0, 5, 0, 333), 60 * 5 * 1e6 + 333],
])
def test_time_to_microseconds(value, expected_microseconds):
    assert time_to_microseconds(value) == expected_microseconds


@pytest.mark.parametrize('value,precision', [
    [time(1), TimePrecision.HOUR],
    [time(1, 20), TimePrecision.MINUTE],
    [time(1, 20, 33), TimePrecision.SECOND],
    [time(1, 20, 33, 125), TimePrecision.MICROSECOND],
])
def test_get_time_precision(value, precision):
    assert get_time_precision(value) == precision
