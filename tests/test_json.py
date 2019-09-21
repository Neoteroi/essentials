import uuid
import pytest
from pytest import raises
from datetime import datetime, date, time
from essentials.json import dumps


@pytest.mark.parametrize('value,expected_json', [
    ({'value': time(10, 30, 15)}, '{"value": "10:30:15"}'),
    ({'value': date(2016, 3, 26)}, '{"value": "2016-03-26"}'),
    ({'value': datetime(2016, 3, 26, 3, 0, 0)}, '{"value": "2016-03-26T03:00:00"}'),
    ({'value': uuid.UUID('e56fddfc-f85b-4178-869f-a218278a639e')}, '{"value": "e56fddfc-f85b-4178-869f-a218278a639e"}'),
    ({'value': b'Lorem ipsum dolor sit amet'}, '{"value": "TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQ="}'),
])
def test_datetime_serialization(value, expected_json):
    data = dumps(value)
    assert expected_json == data


def test_class_with_to_dict_method():

    class Example:

        def __init__(self, x, y):
            self.x = x
            self.y = y

        def to_dict(self):
            return {
                'x': self.x,
                'y': self.y,
                'something_else': True,
                'date': date(2016, 3, 26)
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
