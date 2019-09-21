"""
This module contains an implementation of models annotations, useful to implement validation of business objects
and input values in a consistent way.
It implements a pattern described in Fluent Python by Luciano Ramalho (Chapters 20 and 21).
It uses "Template Method" design pattern and metaprogramming.
This enables interesting features such as automatic generation of __init__ methods for models that define
properties for their instances, removing a lot of boring code.
"""
import re
import os
import uuid
import decimal
import inspect
from typing.re import Pattern
from datetime import datetime, date, time
from collections.abc import Mapping, Iterable
from essentials.typesutils import dateutils
from essentials.folders import ensure_folder
from essentials.exceptions import InvalidArgument, EmptyArgumentException, InvalidOperation


if __debug__:
    ensure_folder('built')


def _generalize_init_type_error_message(ex: TypeError):
    return str(ex)\
        .replace('__init__() ', '')\
        .replace('keyword argument', 'parameter') \
        .replace('keyword arguments', 'parameters') \
        .replace('positional arguments', 'parameters')\
        .replace('positional argument', 'parameter')


def _get_rx(pattern):
    if isinstance(pattern, Pattern):
        return pattern
    if isinstance(pattern, str):
        return re.compile(pattern)
    raise InvalidArgument('Expected str or pattern')


class AutoStorage:

    __counter = 0

    def __init__(self, **kwargs):
        # NB: this function enables using these descriptors
        # without inheriting from Model class
        # This solution is less elegant and overriden by a more elegant solution (metaclassing),
        # when using the Model class
        storage_name = kwargs.get('name', None)
        if not storage_name:
            cls = self.__class__
            storage_name = f'_{cls.__name__}#{cls.__counter}'
            cls.__counter += 1
        self.property_name = storage_name
        self.storage_name = storage_name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.storage_name]

    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = value


class Validated(AutoStorage):
    default_nullable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nullable = kwargs.get('nullable', self.default_nullable)

    def __set__(self, instance, value):
        if self.nullable and value is None:
            super().__set__(instance, value)
            return
        self.base_validate(instance, value)
        value = self.validate(instance, value)
        super().__set__(instance, value)

    def base_validate(self, instance, value):
        if not self.nullable and value is None:
            raise EmptyArgumentException(self.property_name)

    def validate(self, instance, value):
        """return validated value or raise InvalidArgument"""


def _get_dynamic_init(cls, properties):
    # same approach as built-in namedtuple: we use exec to gey a dynamic __init__ method
    # for models that have defined properties but not defined __init__
    args_code = ',\n             '.join(properties)
    cls_full_name = f'{cls.__module__}.{cls.__name__}'
    lines = [
        f'# Code generated automatically by `rocore.models.py`, do not change this code by hand!\n',
        f'# __init__ method for class {cls_full_name}\n\n\n',
        f'def __init__(self,\n             {args_code}):\n']
    for name in properties:
        lines.append(f'    self.{name} = {name}\n')

    lines.append('\n')
    code = ''.join(lines)
    ldict = {}

    if __debug__:
        # create files dynamically,
        # to support debugging into dynamic __init__ functions
        init_file_name = f'built/{cls_full_name}_init_.py'
        with open(init_file_name, encoding='utf8', mode='wt') as init_file:
            init_file.write(code)
            code_block = compile(code, os.path.realpath(init_file.name), 'exec')
            exec(code_block, ldict)
    else:
        exec(code, globals(), ldict)

    return ldict['__init__']


class ModelMeta(type):

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)

        properties = []

        for key, attr in attr_dict.items():
            if isinstance(attr, Validated):
                properties.append(key)
                attr.property_name = key
                attr.storage_name = f'_{type(attr).__name__}#{key}'

        disable_auto_init = os.environ.get('ROCOREDISABLEEXEC')

        if disable_auto_init:
            # automatic __init__ methods with exec are disabled by environmental variable
            return

        if cls.__init__ is object.__init__ and properties:
            setattr(cls, '__init__', _get_dynamic_init(cls, properties))


class Model(metaclass=ModelMeta):
    """Business model with validated entities."""

    @classmethod
    def from_dict(cls, data):
        if data is None:
            raise InvalidArgument('Missing input data')
        try:
            return cls(**data)
        except TypeError as ex:
            raise InvalidArgument('Invalid input: ' + _generalize_init_type_error_message(ex))


class EmptyStringError(InvalidArgument):
    def __init__(self, name):
        super().__init__(f'Value `{name}` cannot be empty or blank.')


class InvalidPatternError(InvalidArgument):
    def __init__(self, value, expected_pattern: Pattern):
        super().__init__(f'Value `{value}` does not respect expected pattern: {expected_pattern.pattern}')


class ExpectedTypeError(InvalidArgument):
    def __init__(self, name, expected_type):
        super().__init__(f'Value `{name}` must be of type'
                         f' {expected_type.__name__ if hasattr(expected_type, "__name__") else expected_type}')


class ExpectedSubclassOfTypeError(InvalidArgument):
    def __init__(self, name, expected_type):
        super().__init__(f'Value `{name}` must be of a type '
                         f'subclassing from '
                         f'{expected_type.__name__ if hasattr(expected_type, "__name__") else expected_type}')


class ExpectedCallableError(InvalidArgument):
    def __init__(self, name):
        super().__init__(f'Value `{name}` must be a callable')


class LengthValidatable:

    def validate_length(self, value):
        try:
            l = len(value)
        except TypeError as te:
            raise InvalidOperation(f'Cannot use as `LengthValidatable`: {str(te)}')

        max_length = self.max_length
        min_length = self.min_length
        if max_length is not None and max_length == min_length and l != max_length:
            raise InvalidArgument(f'Value `{self.property_name}` must be exactly {max_length} long.')
        if max_length is not None and l > max_length:
            raise InvalidArgument(f'Value `{self.property_name}` cannot be longer than {max_length}.')
        if min_length is not None and  l < min_length:
            raise InvalidArgument(f'Value `{self.property_name}` cannot be shorter than {min_length}.')


class RangeValidatable:

    def validate_range(self, value):
        max_value = self.max_value
        min_value = self.min_value
        if max_value is not None and value > max_value:
            raise InvalidArgument(f'Value `{self.property_name}` cannot be greater than {max_value}.')
        if min_value is not None and value < min_value:
            raise InvalidArgument(f'Value `{self.property_name}` cannot be smaller than {str(min_value)}.')


class Callable(Validated):

    def validate(self, instance, value):
        if value is None:
            return value
        if not callable(value):
            raise ExpectedCallableError(self.property_name)
        return value


class OfType(Validated):

    def __init__(self,
                 required_type,
                 **kwargs):
        super().__init__(**kwargs)
        if required_type is None:
            raise EmptyArgumentException('required_type')

        if not inspect.isclass(required_type):
            raise InvalidArgument('expected a type')

        self.required_type = required_type

    def validate(self, instance, value):
        if value is None:
            return value
        if isinstance(value, Mapping) and issubclass(self.required_type, Model):
            return self.required_type.from_dict(value)
        if not isinstance(value, self.required_type):
            raise ExpectedTypeError(self.property_name, self.required_type)
        return value


class SubclassOf(Validated):

    def __init__(self,
                 ancestor_type,
                 **kwargs):
        super().__init__(**kwargs)
        if ancestor_type is None:
            raise EmptyArgumentException('required_type')

        if not inspect.isclass(ancestor_type):
            raise InvalidArgument('expected a class type')

        self.ancestor_type = ancestor_type

    def validate(self, instance, value):
        if value is None:
            return value

        try:
            if not issubclass(value, self.ancestor_type):
                raise ExpectedSubclassOfTypeError(self.property_name, self.ancestor_type)
        except TypeError:
            raise ExpectedSubclassOfTypeError(self.property_name, self.ancestor_type)

        return value


class Anything(Validated):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, instance, value):
        return value


class Boolean(Validated):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, instance, value):
        return bool(value)


class Guid(Validated):

    default_nullable = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, instance, value):
        if isinstance(value, uuid.UUID):
            return value

        if isinstance(value, str):
            try:
                return uuid.UUID(value)
            except ValueError:
                raise ExpectedTypeError(self.property_name, uuid.UUID)

        raise ExpectedTypeError(self.property_name, uuid.UUID)


class TimeValidated(Validated, RangeValidatable):
    def __init__(self, desired_type, max_value=None, min_value=None, **kwargs):
        super().__init__(**kwargs)
        self._desired_type = desired_type
        self.max_value = max_value
        self.min_value = min_value

    def validate(self, instance, value):
        if isinstance(value, str):
            try:
                value = dateutils.parse(value, self._desired_type)
            except ValueError:
                raise ExpectedTypeError(self.property_name, self._desired_type)

        if isinstance(value, Iterable):
            try:
                value = self._desired_type(*value)
            except ValueError:
                raise ExpectedTypeError(self.property_name, self._desired_type)

        if not isinstance(value, self._desired_type):
            raise ExpectedTypeError(self.property_name, self._desired_type)
        self.validate_range(value)
        return value


class Time(TimeValidated):
    def __init__(self, max_value=None, min_value=None, **kwargs):
        super().__init__(time, max_value, min_value, **kwargs)


class Date(TimeValidated):
    def __init__(self, max_value=None, min_value=None, **kwargs):
        super().__init__(date, max_value, min_value, **kwargs)


class DateTime(TimeValidated):
    def __init__(self, max_value=None, min_value=None, **kwargs):
        super().__init__(datetime, max_value, min_value, **kwargs)


class String(Validated, LengthValidatable):

    def __init__(self,
                 max_length=None,
                 min_length=None,
                 allow_blank=True,
                 formatter=str.strip,
                 pattern=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length
        self.min_length = min_length
        self.allow_blank = allow_blank
        self.formatter = formatter
        self.pattern = _get_rx(pattern) if pattern else None

    def validate(self, instance, value):
        if value is None:
            if not self.allow_blank:
                raise EmptyStringError(self.property_name)
            return value
        if isinstance(value, bytes):
            value = value.decode('utf8')

        value = str(value)
        if not self.allow_blank:
            value = value.strip()
            if not value:
                raise EmptyStringError(self.property_name)

        if self.pattern and not self.pattern.search(value):
            raise InvalidPatternError(value, self.pattern)

        if self.formatter:
            value = self.formatter(value)

        self.validate_length(value)
        return value


class Numeric(Validated, RangeValidatable):
    def __init__(self, numeric_type, max_value=None, min_value=None, **kwargs):
        super().__init__(**kwargs)
        self.numeric_type = numeric_type
        self.max_value = max_value
        self.min_value = min_value

    def validate(self, instance, value):
        if not isinstance(value, self.numeric_type):
            raise ExpectedTypeError(self.property_name, self.numeric_type)
        self.validate_range(value)
        return self.numeric_type(value)


class Float(Numeric):
    def __init__(self, max_value=None, min_value=None, **kwargs):
        super().__init__(float, max_value, min_value, **kwargs)


class Int(Numeric):
    def __init__(self, max_value=None, min_value=None, **kwargs):
        super().__init__(int, max_value, min_value, **kwargs)


class Decimal(Numeric):
    def __init__(self, max_value=None, min_value=None, **kwargs):
        super().__init__(decimal.Decimal, max_value, min_value, **kwargs)


class UInt(Numeric):
    def __init__(self, max_value=None, **kwargs):
        super().__init__(int, max_value, 0, **kwargs)


class AnyOf(Validated):

    def __init__(self, possible_values, **kwargs):
        super().__init__(**kwargs)
        self.possible_values = set(possible_values)

    def validate(self, instance, value):
        if value not in self.possible_values:
            raise InvalidArgument('Value must be one of: {}'.format(', '.join(str(x) for x in self.possible_values)))
        return value


class Enum(Validated):

    def __init__(self, enum_type, **kwargs):
        super().__init__(**kwargs)
        self.enum_type = enum_type

    def validate(self, instance, value):
        try:
            return self.enum_type(value)
        except ValueError:
            try:
                return self.enum_type[value]
            except KeyError:
                raise InvalidArgument(f'Value {value} is not valid')


class Collection(Validated, LengthValidatable):

    def __init__(self,
                 model=None,
                 max_length=None,
                 min_length=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.max_length = max_length
        self.min_length = min_length

    def develop_array(self, value):
        for item in value:
            if isinstance(item, self.model):
                yield item
            elif isinstance(item, Mapping):
                yield self.model.from_dict(item)
            else:
                raise InvalidArgument(f'Invalid item in collection: {item}')

    def validate(self, instance, value):
        if isinstance(value, (str, bytes)):
            raise ExpectedTypeError(self.property_name, 'non string and non bytes')

        if not isinstance(value, Iterable):
            raise ExpectedTypeError(self.property_name, 'iterable')

        if self.model:
            value = list(self.develop_array(value))

        self.validate_length(value)
        return value

