import reprlib
from abc import ABC
from typing import List, Sequence, Type

from essentials.exceptions import InvalidArgument


class RegistryException(Exception):
    """Base class for Registry exceptions"""


class AmbiguousRegistryName(RegistryException):
    def __init__(self, name: str, found_types: Sequence[Type]) -> None:
        super().__init__(
            f"The name `{name}` is ambiguous. Found the following types: "
            f'{", ".join(_type.__name__ for _type in found_types)}'
        )


class TypeNotFoundException(RegistryException):
    def __init__(self, name: str, base_class_name: str) -> None:
        super().__init__(f"Type not found: `{name}` for class `{base_class_name}`")


class Registry(ABC):
    @classmethod
    def get_class(cls) -> Type["Registry"]:
        if cls is Registry:
            raise ValueError("Cannot call get_class_name on a Registry")
        mro = list(cls.__mro__)
        mro.reverse()
        for i, m in enumerate(mro):
            if m is Registry:
                break
        return mro[i + 1]

    @classmethod
    def _get_class_keyname(cls) -> str:
        a = cls.get_class()
        return a.__name__.lower()

    @classmethod
    def from_configuration(cls, configuration, cls_type=None) -> "Registry":
        if cls is Registry:
            raise InvalidArgument("call this method with a subclass of `Registry`")

        if isinstance(configuration, str):
            configuration = {"type": configuration}

        if cls_type is None:
            try:
                cls_type = cls._get_type(configuration)
            except (TypeError, ValueError) as error:
                raise InvalidArgument(
                    f"Invalid {cls._get_class_keyname()} "
                    f"configuration. Details: {str(error)}"
                )

        try:
            return cls_type.from_dict(configuration)
        except Exception as error:

            raise InvalidArgument(
                f"Invalid {cls._get_class_keyname()} configuration. "
                f"Cannot create an instance of {cls_type.__name__} "
                f"using the input dictionary `{reprlib.repr(configuration)}`."
                f" Details: {str(error)}"
            )

    @classmethod
    def from_dict(cls, data) -> "Registry":
        a = dict(data)
        del a["type"]
        return cls(**a)

    @classmethod
    def get_class_name(cls) -> str:
        if hasattr(cls, "type_name"):
            return cls.type_name
        key = cls._get_class_keyname()
        length = -len(key)
        s = cls.__name__.lower()
        return s[:length] if s[length:] == key else s

    @classmethod
    def get_subclasses(cls, base_class=None) -> List[Type["Registry"]]:
        if base_class is None:
            base_class = cls.get_class()

        real_subclasses = base_class.__subclasses__()

        all_classes = real_subclasses
        for sub_cls in all_classes:
            all_classes += cls.get_subclasses(sub_cls)

        return all_classes

    @classmethod
    def _get_type(cls, configuration, all_types=None) -> Type["Registry"]:
        try:
            type_name = configuration["type"]
        except TypeError:
            if configuration is None:
                raise InvalidArgument("configuration cannot be null")
            else:
                raise
        except KeyError:
            raise InvalidArgument(
                f"Missing `type` property in configuration object "
                f"{cls._get_class_keyname()}. "
                f"Every configuration describing a {0} must have a `type` property: "
                f"the name of the {reprlib.repr(configuration)} it's referring to."
            )
        if all_types is None:
            all_types = cls.get_subclasses()
        found_types = [
            x
            for x in all_types
            if (
                x.get_class_name() == type_name
                or x.__name__.lower() == type_name.lower()
            )
        ]

        if not found_types:
            raise TypeNotFoundException(type_name, cls.__name__)

        if len(found_types) > 1:
            raise AmbiguousRegistryName(type_name, found_types)

        return found_types[0]
