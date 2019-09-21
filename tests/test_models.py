import re
import uuid
import pytest
import decimal
from datetime import datetime, date, time
from enum import Enum
from pytest import raises
from essentials.exceptions import InvalidArgument, EmptyArgumentException
from essentials.models import (Model,
                           _generalize_init_type_error_message,
                           AnyOf,
                           OfType,
                           Enum as EnumType,
                           String,
                           Int,
                           UInt,
                           Float,
                           Decimal,
                           Guid,
                           Date,
                           DateTime,
                           Time,
                           InvalidPatternError,
                           ExpectedTypeError,
                           Collection,
                           EmptyStringError,
                           Anything,
                           SubclassOf,
                           Boolean,
                           ExpectedSubclassOfTypeError,
                           Callable,
                           ExpectedCallableError)


class Address(Model):
    city = String(allow_blank=False)
    street = String(allow_blank=False)
    zip_code = String(pattern='^\\d{2}-\\d{3}$')
    house_number = Int()
    apartment_number = Int()


class Person(Model):
    id = Guid(nullable=False)
    first_name = String(nullable=False)
    last_name = String(nullable=False)


class Foo(Model):

    def __init__(self, a, b):
        pass


class Ufo(Model):

    def __init__(self, z):
        pass


class FooFoo(Model):

    def __init__(self, a, b, c, d, e, f):
        pass


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class IterableClass:

    def __len__(self):
        return 3

    def __iter__(self):
        yield 'Hello'
        yield 'World'
        yield 'Lorem'


@pytest.mark.parametrize('error_message,expected_message', [
    ("__init__() got an unexpected keyword argument 'e'",
     "got an unexpected parameter 'e'"),
    ("__init__() missing 1 required positional argument: 'a'",
     "missing 1 required parameter: 'a'"),
    ("__init__() missing 2 required positional arguments: 'a' and 'b'",
     "missing 2 required parameters: 'a' and 'b'"),
    ("__init__() missing 6 required positional arguments: 'a', 'b', 'c', 'd', 'e', and 'f'",
     "missing 6 required parameters: 'a', 'b', 'c', 'd', 'e', and 'f'")
])
def test_generalization_of_init_type_error_message(error_message, expected_message):
    value = _generalize_init_type_error_message(TypeError(error_message))
    assert expected_message == value


@pytest.mark.parametrize('_type,params,expected_message', [
    (Foo, {
        'a': True, 'e': 40
    }, "Invalid input: got an unexpected parameter 'e'"),
    (Foo, {
        'b': True
    }, "Invalid input: missing 1 required parameter: 'a'"),
    (Foo, {

    }, "Invalid input: missing 2 required parameters: 'a' and 'b'"),
    (FooFoo, {

    }, "Invalid input: missing 6 required parameters: 'a', 'b', 'c', 'd', 'e', and 'f'"),
    (FooFoo, {
        'a': True
    }, "Invalid input: missing 5 required parameters: 'b', 'c', 'd', 'e', and 'f'"),
    (Foo, {
        'a': 1, 'b': 1, 'c': 2
    }, "Invalid input: got an unexpected parameter 'c'"),
    (Ufo, {
        'a': 1
    }, "Invalid input: got an unexpected parameter 'a'")
])
def test_missing_parameters_for_client_input(_type, params, expected_message):
    with pytest.raises(InvalidArgument) as context:
        _type.from_dict(params)

    assert expected_message == str(context.value)


@pytest.mark.parametrize('value,expected_result',
[
    ('Hello, World', 'Hello, World'),
    ('   Hello, World', 'Hello, World'),
    ('   Hello, World  ', 'Hello, World'),
    (100, '100'),
    (False, 'False'),
    (b'foo', 'foo'),
    (None, None),
])
def test_string_property(value, expected_result):

    class Example(Model):
        name = String()

        def __init__(self, name):
            self.name = name

    instance = Example(value)
    assert instance.name == expected_result


@pytest.mark.parametrize('value,raises',
[
    ('a', True),
    ('               a         ', True),
    ('Hello, World', False),
    ('1234567890', False),
    ('   Hello, World', False),
    ('   Hello, World  ', False),
    (100, True),
    (False, True),
    (b'foo', True),
    (None, False),
])
def test_string_property_min_length_validation(value, raises):

    class Example(Model):
        name = String(min_length=10)

        def __init__(self, name):
            self.name = name

    if raises:
        with pytest.raises(InvalidArgument):
            Example(value)
    else:
        instance = Example(value)
        assert instance is not None


@pytest.mark.parametrize('value,raises',
[
    ('a', False),
    ('               a         ', False),
    ('Hello, World', True),
    ('   Hello, World', True),
    ('   Hello, World  ', True),
    (100, False),
    (False, True),
    (b'foo', False),
    (None, False),
])
def test_string_property_max_length_validation(value, raises):

    class Example(Model):
        name = String(max_length=3)

        def __init__(self, name):
            self.name = name

    if raises:
        with pytest.raises(InvalidArgument):
            Example(value)
    else:
        instance = Example(value)
        assert instance is not None


@pytest.mark.parametrize('value,raises',
[
    ('a', True),
    ('               a         ', True),
    ('Hello, World', True),
    ('   Hello, World', True),
    ('   Hello, World  ', True),
    ('   Hello!  ', False),
    (100, False),
    (False, False),
    (b'foo', False),
    (None, False),
])
def test_string_property_min_max_length_validation(value, raises):

    class Example(Model):
        name = String(min_length=3, max_length=6)

        def __init__(self, name):
            self.name = name

    if raises:
        with pytest.raises(InvalidArgument):
            Example(value)
    else:
        instance = Example(value)
        assert instance is not None


@pytest.mark.parametrize('value,expected_pattern,raises',
[
    ('Hello, World', 'Hello, World', False),
    ('Hello', '^[a-zA-Z]+$', False),
    ('Hello!', '^[a-zA-Z]+$', True),
    ('Hello', '^[a-z]+$', True),
    ('Hello', re.compile('^[a-z]+$', re.I), False),
    ('02-776', '^[0-9]{2}-[0-9]{3}$', False),
    ('02-77', '^[0-9]{2}-[0-9]{3}$', True),
])
def test_string_property(value, expected_pattern, raises):

    class Example(Model):
        name = String(pattern=expected_pattern)

        def __init__(self, name):
            self.name = name

    if raises:
        with pytest.raises(InvalidPatternError):
            Example(value)
    else:
        Example(value)


@pytest.mark.parametrize('value,raises',
[
    (0, False),
    (1, False),
    (20, False),
    (-30, False),
    ('Hello!', True),
    (10.50, True),
    (decimal.Decimal(10.444), True),
    (False, False),
    (True, False),
])
def test_int_property(value, raises):

    class Example(Model):
        value = Int()

        def __init__(self, value):
            self.value = value

    if raises:
        with pytest.raises(ExpectedTypeError):
            Example(value)
    else:
        Example(value)


@pytest.mark.parametrize('value,raises',
[
    (0, True),
    (0.0, False),
    (1, True),
    (1.0, False),
    (-5.4, False),
    ('Hello!', True),
    (10.50, False),
    (decimal.Decimal(10.444), True),
    (False, True),
    (True, True),
])
def test_float_property(value, raises):

    class Example(Model):
        value = Float()

        def __init__(self, value):
            self.value = value

    if raises:
        with pytest.raises(ExpectedTypeError):
            Example(value)
    else:
        Example(value)


@pytest.mark.parametrize('value,raises',
[
    (0, False),
    (1, False),
    (-1, True),
    (20, False),
    (-30, True),
    ('Hello!', True),
    (10.50, True),
    (decimal.Decimal(10.444), True),
    (False, False),
    (True, False),
])
def test_uint_property(value, raises):

    class Example(Model):
        value = UInt()

        def __init__(self, value):
            self.value = value

    if raises:
        with pytest.raises(InvalidArgument):
            Example(value)
    else:
        Example(value)


@pytest.mark.parametrize('value,raises',
[
    (0, True),
    (1, True),
    (-1, True),
    (20, True),
    (-30, True),
    ('Hello!', True),
    (decimal.Decimal('10.5'), False),
    (decimal.Decimal(10.444), False),
    (False, True),
    (True, True),
])
def test_decimal_property(value, raises):

    class Example(Model):
        value = Decimal()

        def __init__(self, value):
            self.value = value

    if raises:
        with pytest.raises(InvalidArgument):
            Example(value)
    else:
        Example(value)


@pytest.mark.parametrize('values,value,raises',
[
    ({1, 2, 3, 4}, 5, True),
    ({1, 2, 3, 4}, 1, False),
    ({'a', 'b', 'c'}, 'b', False),
])
def test_anyof_property(values, value, raises):

    class Example(Model):
        value = AnyOf(values)

        def __init__(self, value):
            self.value = value

    if raises:
        with pytest.raises(InvalidArgument):
            Example(value)
    else:
        Example(value)


@pytest.mark.parametrize('enum_type,value,raises,expected_result',
[
    (Color, 'RED', False, Color.RED),
    (Color, 1, False, Color.RED),
    (Color, 2, False, Color.GREEN),
    (Color, 'YELLOW', True, None),
    (Color, 4, True, None),
])
def test_enum_property(enum_type, value, raises, expected_result):

    class Example(Model):
        value = EnumType(enum_type)

        def __init__(self, value):
            self.value = value

    if raises:
        with pytest.raises(InvalidArgument):
            Example(value)
    else:
        Example(value)


@pytest.mark.parametrize('value,raises',
[
    (Color, False),
    ({1,2,3,4,5}, False),
    ([1, 2, 3, 4, 5], False),
    (range(10), False),
    ("Hello, World", True),
    (b"Hello, World", True),
    (1, True),
    (2.2, True),
    (IterableClass(), False)
])
def test_collection_property(value, raises):

    class Example(Model):
        value = Collection()

        def __init__(self, value):
            self.value = value

    if raises:
        with pytest.raises(InvalidArgument):
            Example(value)
    else:
        Example(value)


@pytest.mark.parametrize('value,min_length,raises',
[
    ({1,2,3,4,5}, 7, True),
    ([1, 2, 3, 4, 5], 6, True),
    ([1, 2, 3, 4, 5], 5, False),
    ([1, 2, 3, 4, 5], 3, False),
    (range(5), 6, True),
    (range(10), 6, False),
    (IterableClass(), 10, True)
])
def test_collection_property_with_min_length(value, min_length, raises):

    class Example(Model):
        value = Collection(min_length=min_length)

        def __init__(self, value):
            self.value = value

    if raises:
        with pytest.raises(InvalidArgument):
            Example(value)
    else:
        Example(value)


@pytest.mark.parametrize('value,max_length,raises',
[
    ({1,2,3,4,5}, 7, False),
    ([1, 2, 3, 4, 5], 6, False),
    ([1, 2, 3, 4, 5], 5, False),
    ([1, 2, 3, 4, 5], 3, True),
    (range(5), 6, False),
    (range(10), 6, True),
    (IterableClass(), 2, True)
])
def test_collection_property_with_max_length(value, max_length, raises):

    class Example(Model):
        value = Collection(max_length=max_length)

        def __init__(self, value):
            self.value = value

    if raises:
        with pytest.raises(InvalidArgument):
            Example(value)
    else:
        Example(value)


@pytest.mark.parametrize('model_type,values,raises',
[
    (Address, {
        'city': 'Warszawa',
        'street': 'Pokorna',
        'zip_code': '03-444',
        'house_number': 2,
        'apartment_number': 60
    }, False),
    (Address, {
        'street': 'Pokorna',
        'zip_code': '03-444',
        'house_number': 2,
        'apartment_number': 60
    }, True),
])
def test_model_validation(model_type, values, raises):

    if raises:
        with pytest.raises(InvalidArgument):
            model_type.from_dict(values)
    else:
        instance = model_type.from_dict(values)

        assert instance is not None
        assert instance.city == values.get('city')
        assert instance.street == values.get('street')
        assert instance.zip_code == values.get('zip_code')
        assert instance.house_number == values.get('house_number')
        assert instance.apartment_number == values.get('apartment_number')


class ChildModel(Model):
    name = String(nullable=False)


class ParentModel(Model):
    name = String(nullable=False)
    child = OfType(ChildModel, nullable=False)


def test_child_model():

    with pytest.raises(InvalidArgument):
        ParentModel('example', None)

    with pytest.raises(InvalidArgument):
        ParentModel('example', ChildModel(None))

    instance = ParentModel('example', ChildModel('child_name'))

    assert instance is not None
    assert isinstance(instance.child, ChildModel)
    assert instance.name == 'example'
    assert instance.child.name == 'child_name'


def test_child_model_from_dict():

    data_from_json_example = {
        'name': 'example',
        'child': {
            'name': 'child_name'
        }
    }

    instance = ParentModel.from_dict(data_from_json_example)

    assert instance is not None
    assert isinstance(instance.child, ChildModel)
    assert instance.name == 'example'
    assert instance.child.name == 'child_name'


@pytest.mark.parametrize('model_type,value,raises',
[
    (Person, [
        Person('0fb59f3e-fb5a-404f-9798-afcc4e07fb82', 'Roberto', 'Prevato'),
        Person('193596ce-68fc-4c49-a106-19978763d3ca', 'Paolo', 'Rossi'),
        Person('b4597c50-fb0e-4238-85ac-07801d59bc14', 'Jan', 'Kowalski')
    ], False),
    (int, [1, 2, 3, 4, 5], False),
    (int, [1, 2, 3, 4, 'nope'], True),
    (str, ['Lorem', 'ipsum', 'dolor', 'sit', 'amet'], False),
    ((str, int), ['Lorem', 10, 'ipsum', 12, 'dolor', 'sit', 'amet', 10], False),
    (str, ['Lorem', 'ipsum', 'dolor', 'sit', 0], True),
    (Person, [
        {'id': '0fb59f3e-fb5a-404f-9798-afcc4e07fb82', 'first_name': 'Roberto', 'last_name': 'Prevato'},
        {'id': '193596ce-68fc-4c49-a106-19978763d3ca', 'first_name': 'Paolo', 'last_name': 'Rossi'},
        {'id': 'b4597c50-fb0e-4238-85ac-07801d59bc14', 'first_name': 'Jan', 'last_name': 'Kowalski'}
    ], False),
    (Person, [], False),
    (Person, [
        {'id': 'da26a15f-1c4e-457c-ad55-3205e7d3816d'},
        {'first_name': 'Paolo'}
    ], True),
    (Person, [
        'Lorem', 'ipsum'
    ], True),
])
def test_collection_property_with_model(model_type, value, raises):

    class Example(Model):
        value = Collection(model_type)

        def __init__(self, value):
            self.value = value

    if raises:
        with pytest.raises(InvalidArgument):
            Example(value)
    else:
        instance = Example(value)

        assert instance is not None
        assert len(instance.value) == len(value)


@pytest.mark.parametrize('value,expected_result',
[
    (uuid.UUID('da26a15f-1c4e-457c-ad55-3205e7d3816d'), uuid.UUID('da26a15f-1c4e-457c-ad55-3205e7d3816d')),
    ('da26a15f-1c4e-457c-ad55-3205e7d3816d', uuid.UUID('da26a15f-1c4e-457c-ad55-3205e7d3816d')),
])
def test_guid_property(value, expected_result):

    class Example(Model):
        name = Guid()

        def __init__(self, name):
            self.name = name

    instance = Example(value)
    assert instance.name == expected_result


def test_guid_property_default_not_nullable():

    class Example(Model):
        id = Guid()

        def __init__(self, _id):
            self.id = _id

    with pytest.raises(EmptyArgumentException):
        Example(None)


@pytest.mark.parametrize('value,expected_result',
[
    ('10:20:15', time(10, 20, 15)),
    (time(10, 20, 15), time(10, 20, 15)),
    ('05:30', time(5, 30, 0)),
])
def test_time_property(value, expected_result):

    class Example(Model):
        value = Time()

        def __init__(self, value):
            self.value = value

    instance = Example(value)
    assert instance.value == expected_result


@pytest.mark.parametrize('value,expected_result',
[
    ('2018-05-30', date(2018, 5, 30)),
    (date(2018, 5, 30), date(2018, 5, 30)),
    ('2018-02-10', date(2018, 2, 10)),
])
def test_date_property(value, expected_result):

    class Example(Model):
        value = Date()

        def __init__(self, value):
            self.value = value

    instance = Example(value)
    assert instance.value == expected_result


@pytest.mark.parametrize('value,expected_result',
[
    ('2018-05-30 10:20:15', datetime(2018, 5, 30, 10, 20, 15)),
    (datetime(2018, 5, 30, 10, 20, 15), datetime(2018, 5, 30, 10, 20, 15)),
    ('2018-02-10 05:30:00', datetime(2018, 2, 10, 5, 30, 0)),
])
def test_datetime_property(value, expected_result):

    class Example(Model):
        value = DateTime()

        def __init__(self, value):
            self.value = value

    instance = Example(value)
    assert instance.value == expected_result


def test_non_blank_string_raises_for_blank_value():

    class X(Model):
        value = String(allow_blank=False, nullable=False)

    with raises(EmptyStringError):
        string_prop = String(allow_blank=False)
        string_prop.validate(None, None)

    with raises(EmptyStringError):
        X('  ')


def test_blankable_string_does_not_raises_for_blank_value():
    string_prop = String(allow_blank=True)
    string_prop.validate(None, None)


def test_time_raises_for_invalid_str():
    prop = Time()

    with raises(ExpectedTypeError):
        prop.validate(None, 'XXX')


def test_time_raises_for_invalid_iterable():
    prop = Time()

    with raises(ExpectedTypeError):
        prop.validate(None, (-1999,))


def test_time_raises_for_invalid_type():
    prop = Time()

    with raises(ExpectedTypeError):
        prop.validate(None, 23)


def test_guid_aises_for_invalid_str():
    prop = Guid()

    with raises(ExpectedTypeError):
        prop.validate(None, 'xxx')


def test_guid_aises_for_invalid_type():
    prop = Guid()

    with raises(ExpectedTypeError):
        prop.validate(None, False)


def test_anything():
    prop = Anything()

    prop.validate(None, 10)
    prop.validate(None, 'AAA')
    prop.validate(None, False)
    prop.validate(None, [])


def test_bool():
    prop = Boolean()

    assert prop.validate(None, 1) is True
    assert prop.validate(None, True) is True
    assert prop.validate(None, 0) is False
    assert prop.validate(None, None) is False


def test_subclass_of():
    class A:
        pass

    class B(A):
        pass

    class C(B):
        pass

    prop = SubclassOf(A)

    assert prop.validate(None, B) is B
    assert prop.validate(None, C) is C


def test_subclass_of_raises_for_invalid_type():
    class A:
        pass

    class B:
        pass

    prop = SubclassOf(A)

    with raises(ExpectedSubclassOfTypeError):
        assert prop.validate(None, B)


def test_subclass_of_raises_for_invalid_value_type():
    class A:
        pass

    prop = SubclassOf(A)

    with raises(ExpectedSubclassOfTypeError):
        assert prop.validate(None, 3)


def test_subclass_of_allows_none():
    class A:
        pass

    prop = SubclassOf(A)

    assert prop.validate(None, None) is None


def test_subclass_of_raises_for_missing_argument():
    with raises(EmptyArgumentException):
        SubclassOf(None)


def test_subclass_of_raises_for_invalid_argument():
    with raises(InvalidArgument):
        SubclassOf(100)


def test_model_from_dict_raises_for_none():
    class A(Model):
        value = String()

    with raises(InvalidArgument):
        A.from_dict(None)


def test_model_callable_raises_for_non_callable():
    class A(Model):
        value = Callable()

    with raises(ExpectedCallableError):
        A(False)


def test_model_callable_accepts_null():
    prop = Callable()
    assert prop.validate(None, None) is None


def test_model_callable():
    prop = Callable()

    def fn():
        pass

    assert prop.validate(None, fn) is fn


def test_of_type_raises_for_none():
    with raises(EmptyArgumentException):
        OfType(None)


def test_of_type_raises_for_non_class():
    with raises(InvalidArgument):
        OfType(1)


def test_of_type_allows_none():
    prop = OfType(Address)

    assert prop.validate(None, None) is None


def test_of_type_raises_for_wrong_type():
    class A:
        pass

    class B:
        pass

    prop = OfType(A)

    with raises(ExpectedTypeError):
        prop.validate(None, B)
