from pytest import raises

from essentials.exceptions import InvalidArgument
from essentials.registry import AmbiguousRegistryName, Registry, TypeNotFoundException


def test_registry_type():
    class Rule(Registry):
        pass

    class OneRule(Rule):
        def __init__(self, a, b):
            self.a = a
            self.b = b

    class TwoRule(Rule):
        def __init__(self, c, d):
            self.c = c
            self.d = d

    x = Rule.from_configuration({"type": "one", "a": 10, "b": 20})

    assert isinstance(x, OneRule)
    assert x.a == 10
    assert x.b == 20

    x = Rule.from_configuration({"type": "two", "c": 100, "d": 200})

    assert isinstance(x, TwoRule)
    assert x.c == 100
    assert x.d == 200


def test_registry_type_with_name():
    class Rule(Registry):
        pass

    class OneRule(Rule):
        type_name = "1"

        def __init__(self, a, b):
            self.a = a
            self.b = b

    class TwoRule(Rule):
        type_name = "2"

        def __init__(self, c, d):
            self.c = c
            self.d = d

    x = Rule.from_configuration({"type": "1", "a": 10, "b": 20})

    assert isinstance(x, OneRule)
    assert x.a == 10
    assert x.b == 20

    x = Rule.from_configuration({"type": "2", "c": 100, "d": 200})

    assert isinstance(x, TwoRule)
    assert x.c == 100
    assert x.d == 200


def test_registry_type_with_full_class_name():
    class Rule(Registry):
        pass

    class OneRule(Rule):
        def __init__(self, a, b):
            self.a = a
            self.b = b

    x = Rule.from_configuration({"type": "onerule", "a": 10, "b": 20})

    assert isinstance(x, OneRule)
    assert x.a == 10
    assert x.b == 20


def test_registry_type_subclass():
    class Rule(Registry):
        pass

    class OneRule(Rule):
        def __init__(self, a, b):
            self.a = a
            self.b = b

    class TwoRule(OneRule):
        def __init__(self, c, d):
            super().__init__(None, None)
            self.c = c
            self.d = d

    x = Rule.from_configuration({"type": "two", "c": 100, "d": 200})

    assert isinstance(x, TwoRule)
    assert x.c == 100
    assert x.d == 200


def test_registry_type_parameterless():
    class Rule(Registry):
        pass

    class OneRule(Rule):
        def __init__(self):
            pass

    x = Rule.from_configuration("one")

    assert isinstance(x, OneRule)


def test_registry_type_raises_for_invalid_configuration():
    class Rule(Registry):
        pass

    with raises(InvalidArgument):
        Rule.from_configuration(None)

    with raises(InvalidArgument):
        Rule.from_configuration([])


def test_registry_type_raises_for_invalid_configuration_without_type():
    class Rule(Registry):
        pass

    with raises(
        InvalidArgument, match="Missing `type` property in configuration object"
    ):
        Rule.from_configuration({"foo": "foo"})


# noinspection PyUnusedLocal
def test_registry_raises_for_ambiguous_names():
    class Rule(Registry):
        pass

    class OneRule(Rule):
        pass

    class TwoRule(Rule):
        type_name = "one"

    with raises(AmbiguousRegistryName):
        Rule.from_configuration("one")


# noinspection PyUnusedLocal
def test_registry_raises_for_not_found_type():
    class Rule(Registry):
        pass

    class OneRule(Rule):
        pass

    with raises(TypeNotFoundException):
        Rule.from_configuration("xx")


def test_get_class_raises_on_registry():

    with raises(ValueError):
        Registry.get_class_name()


def test_from_configuration_on_registry_raises():

    with raises(
        InvalidArgument, match="call this method with a subclass of `Registry`"
    ):
        Registry.from_configuration("one")


def test_from_configuration_raises_with_invalid_input():
    class Rule(Registry):
        pass

    class OneRule(Rule):
        pass

    with raises(InvalidArgument):
        Rule.from_configuration(False)


def test_from_configuration_raises_with_invalid_input_for_class():
    class Rule(Registry):
        pass

    class OneRule(Rule):
        def __init__(self, a, b):
            self.a = a
            self.b = b

    with raises(
        InvalidArgument,
        match="Invalid rule configuration. Cannot create an instance of "
        "OneRule using the input dictionary",
    ):
        Rule.from_configuration({"type": "one", "x": 1, "y": 2})
