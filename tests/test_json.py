from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum, Flag, IntEnum, IntFlag, auto
from uuid import UUID, uuid4

import pytest
from pytest import raises

from essentials.json import dumps


@dataclass
class Foo:
    id: UUID
    name: str


class Fruit(Enum):
    ANANAS = "ananas"
    BANANA = "banana"
    MANGO = "mango"


class Power(IntEnum):

    NONE = 0
    MILD = 1
    MODERATE = 2
    GREAT = 3


class Color(Flag):
    RED = auto()
    BLUE = auto()
    GREEN = auto()


class Permission(IntFlag):
    R = 4
    W = 2
    X = 1


@pytest.mark.parametrize(
    "value,expected_json",
    [
        ({"value": time(10, 30, 15)}, '{"value": "10:30:15"}'),
        ({"value": date(2016, 3, 26)}, '{"value": "2016-03-26"}'),
        ({"value": datetime(2016, 3, 26, 3, 0, 0)}, '{"value": "2016-03-26T03:00:00"}'),
        ({"value": Decimal("10.5")}, '{"value": "10.5"}'),
        (
            {"value": UUID("e56fddfc-f85b-4178-869f-a218278a639e")},
            '{"value": "e56fddfc-f85b-4178-869f-a218278a639e"}',
        ),
        (
            {"value": b"Lorem ipsum dolor sit amet"},
            '{"value": "TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQ="}',
        ),
    ],
)
def test_datetime_serialization(value, expected_json):
    data = dumps(value)
    assert expected_json == data


def test_class_with_to_dict_method():
    class Example:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def dict(self):
            return {
                "x": self.x,
                "y": self.y,
                "something_else": True,
                "date": date(2016, 3, 26),
            }

    data = dumps(Example(10, 20))
    assert '{"x": 10, "y": 20, "something_else": true, "date": "2016-03-26"}' == data


def test_raises_for_unhandled_class():
    class Example:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    with raises(Exception):
        dumps(Example(10, 20))


def test_enum_to_json():
    value = dumps(
        {
            "fruit": Fruit.MANGO,
            "favorite_fruits": [Fruit.MANGO, Fruit.ANANAS, Fruit.BANANA],
        }
    )

    assert '"fruit": "mango"' in value
    assert '"favorite_fruits": ["mango", "ananas", "banana"]' in value


def test_int_enum_to_json():
    value = dumps({"power": Power.GREAT, "powers": [Power.MILD, Power.MODERATE]})

    assert '"power": 3' in value
    assert '"powers": [1, 2]' in value


def test_intflag_enum_to_json():
    value = dumps(
        {
            "permission_one": Permission.R,
            "permission_two": Permission.R | Permission.W,
            "permission_three": Permission.W | Permission.X,
        }
    )

    assert '{"permission_one": 4, "permission_two": 6, "permission_three": 3}' == value


def test_flag_enum_to_json():
    value = dumps(
        {
            "color_one": Color.GREEN,
            "color_two": Color.GREEN | Color.RED,
            "color_three": Color.GREEN | Color.RED | Color.BLUE,
        }
    )

    assert '{"color_one": 4, "color_two": 5, "color_three": 7}' == value


def test_serialize_dataclass():
    foo_id = uuid4()
    value = dumps(Foo(foo_id, "foo"))

    assert f'{{"id": "{foo_id}", "name": "foo"}}' == value


def test_serialize_dataclass_no_spaces():
    foo_id = uuid4()
    value = dumps(Foo(foo_id, "foo"), separators=(",", ":"))

    assert f'{{"id":"{foo_id}","name":"foo"}}' == value
