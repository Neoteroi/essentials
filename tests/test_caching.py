import time

import pytest
from essentials.caching import Cache, ExpiringCache, lazy


@pytest.mark.parametrize(
    'cache',
    [Cache(), ExpiringCache(lambda _: False)]
)
def test_cache__getitem_throws_keyerror(cache: Cache):
    with pytest.raises(KeyError):
        cache["cat"]


@pytest.mark.parametrize(
    'cache',
    [Cache(), ExpiringCache(lambda _: False)]
)
def test_cache__setitem__getitem(cache: Cache):
    cache.set("cat", "Celine")
    value = cache.get("cat")

    assert "Celine" == value


@pytest.mark.parametrize(
    'cache',
    [Cache(), ExpiringCache(lambda _: False)]
)
def test_cache_item(cache: Cache):
    cache["cat"] = "Celine"
    value = cache["cat"]

    assert "Celine" == value


@pytest.mark.parametrize(
    'cache',
    [Cache(max_size=3), ExpiringCache(lambda _: False, max_size=3)]
)
def test_reset_existing_item(cache: Cache):
    cache[1] = 1
    cache[2] = 2
    cache[3] = 3
    cache[4] = 4

    assert 1 not in cache

    cache.clear()

    cache[1] = 1
    cache[2] = 2
    cache[3] = 3
    cache[1] = 1
    cache[4] = 4

    assert 2 not in cache
    assert 1 in cache
    assert 3 in cache
    assert 4 in cache


@pytest.mark.parametrize(
    'cache',
    [Cache(max_size=20), ExpiringCache(lambda _: False, max_size=20)]
)
def test_cache_max_size(cache: Cache):
    for i in range(30):
        cache.set(f"key_{i}", i)

    for i in range(10):
        assert f"key_{i}" not in cache

    for i in range(10, 30):
        assert f"key_{i}" in cache


def test_cache_keys_and_values():
    cache = Cache()
    letters = "a b c d e f g".split()

    for index, letter in enumerate(letters):
        cache[letter] = index

    keys = list(cache.keys())
    values = list(cache.values())
    assert keys == list(letters)
    assert values == [index for index in range(len(letters))]


@pytest.mark.parametrize(
    'cache',
    [Cache(max_size=20), ExpiringCache(lambda _: False, max_size=20)]
)
def test_cache_len(cache: Cache):
    for i in range(30):
        cache.set(f"key_{i}", i)

    assert len(cache) == 20


@pytest.mark.parametrize(
    'cache',
    [Cache(), ExpiringCache(lambda _: False)]
)
def test_cache_iterable(cache: Cache):
    for i in range(20):
        cache.set(i, i * i)

    j = 0
    for key, value in cache:
        assert j == key
        assert value == j * j
        j += 1


def test_expiration_policy_with_max_age():
    cache = ExpiringCache.with_max_age(0.1, 5)
    cache['foo'] = 'Foo'

    time.sleep(0.2)

    assert cache.get('foo') is None

    cache['foo'] = 'Foo'

    time.sleep(0.2)

    assert 'foo' not in cache


def test_expiration_policy():
    cache = ExpiringCache(lambda item: item.value > 5)
    for i in range(10):
        cache.set(i, i)
    expired = cache.get(6)
    assert expired is None
    assert 6 not in cache


def test_expiration_policy_when_full():
    cache = ExpiringCache(lambda item: item.value > 1, max_size=2)
    cache.set('a', 1)
    cache.set('b', 2)
    cache.set('c', 0)
    assert cache.get('b') is None
    assert cache.get('a') == 1
    assert cache.get('c') == 0


@pytest.mark.parametrize(
    'cache',
    [Cache(), ExpiringCache(lambda _: False)]
)
def test_cache_clear_is_empty(cache: Cache):
    cache.set("cat", "Celine")
    assert not cache.is_empty

    cache.clear()

    assert cache.is_empty
    assert "cat" not in cache


def test_expiring_cache_checks_expiration_when_iterating():
    cache = ExpiringCache(lambda item: item.value > 4)

    cache["a"] = 1
    cache["b"] = 2
    cache["c"] = 3
    cache["d"] = 4
    cache["e"] = 5
    cache["f"] = 6
    cache["g"] = 1

    values = dict(cache)
    assert "a" in values
    assert "g" in values
    assert "e" not in values
    assert "f" not in values


def test_cache_repr():
    cache = Cache()
    cache['foo'] = ...

    assert repr(cache) == f"<Cache {len(cache)} at {id(cache)}>"


def test_lazy_method():
    i = 0

    @lazy(0.05)
    def increase() -> int:
        nonlocal i
        i += 1
        return i

    for _ in range(10):
        assert increase() == 1

    time.sleep(0.1)

    for _ in range(10):
        assert increase() == 2

    time.sleep(0.1)

    for _ in range(10):
        assert increase() == 3


def test_lazy_method_support_dict_cache():
    cache_one = {}
    cache_two = {}

    @lazy(0.05, cache_one)
    def foo():
        return ...

    @lazy(0.05, cache_two)
    def ofo():
        return ...

    assert foo.cache is cache_one
    assert ofo.cache is cache_two

    foo()
    assert len(cache_one) == 1


def test_lazy_method_cache_depends_on_input_arguments():

    @lazy(100, {})
    def get_object(key):
        return object()

    a = get_object("one")

    assert get_object("one") is a

    b = get_object("two")

    assert a is not b
    assert get_object("one") is a
    assert get_object("two") is b


def test_lazy_method_cache_depends_on_input_arguments_args():

    @lazy(100, {})
    def get_object(*keys):
        return object()

    a = get_object("lorem", "ipsum")

    assert get_object("lorem", "ipsum") is a

    b = get_object("lorem", "ipsum", "dolor")

    assert a is not b
    assert get_object("lorem", "ipsum") is a
    assert get_object("lorem", "ipsum", "dolor") is b
