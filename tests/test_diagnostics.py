import time

import pytest
from pytest import raises

from essentials.diagnostics import StopWatch

DELTA = 0.15


def test_stopwatch():
    a = StopWatch()
    a.start()

    time.sleep(0.01)

    a.stop()
    assert pytest.approx(0.01, DELTA) == a.elapsed_s
    assert pytest.approx(a.elapsed_ms, DELTA) == a.elapsed_s * 1000


def test_stopwatch_with_context_manager():
    with StopWatch() as a:
        time.sleep(0.01)

    assert pytest.approx(0.01, DELTA) == a.elapsed_s
    assert pytest.approx(a.elapsed_ms, DELTA) == a.elapsed_s * 1000


def test_stopwatch_raises_for_start_twice():

    with StopWatch() as sw:

        with raises(RuntimeError, match="StopWatch already running"):
            sw.start()


def test_stopwatch_raises_for_stop_when_not_running():

    sw = StopWatch()
    with raises(RuntimeError, match="StopWatch not running"):
        sw.stop()


def test_stopwatch_reset():
    a = StopWatch()
    a.start()

    time.sleep(0.01)

    a.stop()
    assert a.elapsed_s > 0

    a.reset()

    assert a.elapsed_s == 0.0
    assert a.elapsed_ms == 0.0


def test_stopwatch_repr():
    a = StopWatch()

    assert repr(a) == "<StopWatch elapsed s.: 0.0>"
