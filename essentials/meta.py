import warnings
from functools import wraps
from inspect import iscoroutinefunction
from typing import Callable, Optional, TypeVar

T = TypeVar("T")
FuncType = Callable[..., T]


class DeprecatedException(Exception):
    def __init__(self, param_name: str) -> None:
        super().__init__("The function `%s` is deprecated" % param_name)


def deprecated(
    message: Optional[str] = None, raise_exception=False
) -> Callable[[FuncType], FuncType]:
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used, or optionally an exception raised.
    """
    if message:
        message = " " + message
    else:
        message = ""

    def _deprecated(fn):
        if iscoroutinefunction(fn):

            @wraps(fn)
            async def async_wrapper(*args, **kwargs):
                with warnings.catch_warnings():
                    warnings.simplefilter("always")
                    warnings.warn_explicit(
                        f"`{fn.__name__}` is deprecated.{message}",
                        category=DeprecationWarning,
                        filename=fn.__code__.co_filename,
                        lineno=fn.__code__.co_firstlineno + 1,
                    )
                if raise_exception:
                    raise DeprecatedException(fn.__name__)
                return await fn(*args, **kwargs)

            return async_wrapper

        @wraps(fn)
        def wrapper(*args, **kwargs):
            with warnings.catch_warnings():
                warnings.simplefilter("always")
                warnings.warn_explicit(
                    f"`{fn.__name__}` is deprecated.{message}",
                    category=DeprecationWarning,
                    filename=fn.__code__.co_filename,
                    lineno=fn.__code__.co_firstlineno + 1,
                )
            if raise_exception:
                raise DeprecatedException(fn.__name__)
            return fn(*args, **kwargs)

        return wrapper

    return _deprecated
