"""
Timer class, edited from: Python Cookbook,
3rd Edition by Brian K. Jones, David Beazley
"""
import time


class StopWatch:
    def __init__(self, func=time.perf_counter):
        self._elapsed_s = 0.0
        self._func = func
        self._start = None

    def __repr__(self):
        return f"<StopWatch elapsed s.: {self.elapsed_s}>"

    def start(self):
        if self._start is not None:
            raise RuntimeError("StopWatch already running")

        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError("StopWatch not running")

        self._elapsed_s += self._func() - self._start

    def reset(self):
        self._start = None
        self._elapsed_s = 0.0

    @property
    def elapsed_s(self):
        return self._elapsed_s

    @property
    def elapsed_ms(self):
        if self.elapsed_s > 0.0:
            return self.elapsed_s * 1000
        return 0.0

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()
