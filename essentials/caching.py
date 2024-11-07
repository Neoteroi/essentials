import functools
import time
from collections import OrderedDict
from typing import TYPE_CHECKING, Any, Generic, Iterable, Iterator, Tuple, TypeVar

if TYPE_CHECKING:
    from typing import Callable, TypeVarTuple, Unpack

    PosArgsT = TypeVarTuple("PosArgsT")
    T_Retval = TypeVar("T_Retval")
    FuncType = Callable[[Unpack[PosArgsT]], T_Retval]
    FuncDecoType = Callable[[FuncType], FuncType]

T = TypeVar("T")


class Cache(Generic[T]):
    """In-memory LRU cache implementation."""

    def __init__(self, max_size: int = 500) -> None:
        self._bag: OrderedDict[Any, Any] = OrderedDict()
        self._max_size = -1
        self.max_size = max_size

    @property
    def max_size(self) -> int:
        return self._max_size

    @max_size.setter
    def max_size(self, value: int) -> None:
        assert value > 0
        self._max_size = int(value)

    @property
    def is_empty(self) -> bool:
        return len(self._bag) == 0

    def values(self) -> Iterable[T]:
        for _, value in self:
            yield value

    def keys(self) -> Iterable[Any]:
        for key, _ in self:
            yield key

    def __repr__(self) -> str:
        return f"<Cache {len(self)} at {id(self)}>"

    def __len__(self) -> int:
        return len(self._bag)

    def get(self, key, default=None) -> T:
        try:
            return self[key]
        except KeyError:
            return default

    def set(self, key, value) -> None:
        self[key] = value

    def _check_size(self) -> None:
        while len(self._bag) > self.max_size:
            self._bag.popitem(last=False)

    def __getitem__(self, key) -> T:
        value = self._bag[key]
        self._bag.move_to_end(key, last=True)
        return value

    def __setitem__(self, key, value: T) -> None:
        if key in self._bag:
            self._bag[key] = value
            self._bag.move_to_end(key, last=True)
        else:
            self._bag[key] = value
            self._check_size()

    def __delitem__(self, key) -> None:
        del self._bag[key]

    def __contains__(self, key) -> bool:
        return key in self._bag

    def __iter__(self) -> Iterator[Tuple[Any, T]]:
        return iter(self._bag.items())

    def clear(self) -> None:
        self._bag.clear()


class CachedItem(Generic[T]):
    """Container for cached items with update timestamp."""

    __slots__ = ("_value", "_time")

    def __init__(self, value: T) -> None:
        self._value = value
        self._time = time.time()

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T) -> None:
        self._value = value
        self._time = time.time()

    @property
    def time(self) -> float:
        return self._time


class ExpiringCache(Cache[T]):
    """A cache whose items can expire by a given function."""

    def __init__(
        self, expiration_policy: "Callable[[CachedItem[T]], bool]", max_size: int = 500
    ) -> None:
        super().__init__(max_size)
        assert expiration_policy is not None
        self.expiration_policy = expiration_policy

    @property
    def full(self) -> bool:
        return self.max_size <= len(self._bag)

    def expired(self, item: CachedItem) -> bool:
        return self.expiration_policy(item)

    def _remove_expired_items(self) -> None:
        for key, item in list(self._bag.items()):
            if self.expired(item):
                del self[key]

    def _check_size(self) -> None:
        if self.full:
            self._remove_expired_items()
        super()._check_size()

    def __getitem__(self, key) -> Any:
        item = self._bag[key]
        if self.expired(item):
            del self._bag[key]
            raise KeyError(key)

        self._bag.move_to_end(key, last=True)
        return item.value

    def __setitem__(self, key, value: T) -> None:
        if key in self._bag:
            self._bag[key].value = value
            self._bag.move_to_end(key, last=True)
        else:
            self._bag[key] = CachedItem(value)
            self._check_size()

    @classmethod
    def with_max_age(cls, max_age: float, max_size: int = 500) -> "ExpiringCache":
        """
        Returns an instance of ExpiringCache whose items are invalidated
        when they were set more than a given number of seconds ago.
        """
        return cls(lambda item: time.time() - item.time > max_age, max_size)

    def __contains__(self, key) -> bool:
        if key not in self._bag:
            return False
        # remove if expired
        try:
            self[key]
        except KeyError:
            return False
        return True

    def __iter__(self) -> Iterator[Tuple[Any, T]]:
        """Iterates through cached items, discarding and removing expired ones."""
        for key, item in list(self._bag.items()):
            if self.expired(item):
                del self[key]
            else:
                yield (key, item.value)


def lazy(max_seconds: int = 1, cache=None) -> "FuncDecoType":
    """
    Wraps a function so that it is called up to once
    every max_seconds, by input arguments.
    Results are stored in a cache, by default a LRU cache of max size 500.

    To have a cache without size limit, use a dictionary: @lazy(1, {})
    """
    assert max_seconds > 0
    if cache is None:
        cache = Cache(500)

    def lazy_decorator(fn):
        setattr(fn, "cache", cache)

        @functools.wraps(fn)
        def wrapper(*args):
            now = time.time()
            try:
                value, updated_at = cache[args]
                if now - updated_at > max_seconds:
                    raise AttributeError
            except (KeyError, AttributeError):
                value = fn(*args)
                cache[args] = (value, now)
            return value

        return wrapper

    return lazy_decorator
