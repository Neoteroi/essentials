import pytest
from essentials.meta import DeprecatedException, deprecated


@deprecated()
def dep_method():
    pass


class Sad:

    @deprecated('Sad class is deprecated, don`t use', raise_exception=True)
    def __init__(self):
        pass


def test_class_deprecated_method():
    with pytest.warns(DeprecationWarning, match='`__init__` is deprecated. Sad class is deprecated, don`t use'):
        with pytest.raises(DeprecatedException):
            Sad()


def test_deprecated_method():
    with pytest.warns(DeprecationWarning, match='`dep_method` is deprecated.'):
        dep_method()
