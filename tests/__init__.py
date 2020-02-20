from typing import Any


class CrashTest(RuntimeError):
    def __init__(self, value: Any = ""):
        super().__init__("Crash!" + (f" {value}" if value else ""))
        self.value = value

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        if isinstance(other, CrashTest):
            return self.value == other.value
        return NotImplemented
