from functools import wraps
from inspect import iscoroutinefunction
from typing import Type
from .retry import retry, CatchException, OnException  # noqa


def exception_handle(
    exception_type: Type[Exception],
    catch_exceptions_types: CatchException = None
):
    """
    Wraps a given function to catch all exceptions that might happen during
    its execution, and rethrow new exceptions of the given type.

    :param exception_type: the desired type of exception,
                           to be thrown in case of exception.
    :param catch_exceptions_types: the types of exception to be
                                   catched (defaults to Exception)
    """
    if not catch_exceptions_types:
        catch_exceptions_types = Exception

    def decorator(fn):
        if iscoroutinefunction(fn):

            @wraps(fn)
            async def async_wrapper(*args, **kwargs):
                try:
                    return await fn(*args, **kwargs)
                except catch_exceptions_types as exp:
                    raise exception_type(exp)

            return async_wrapper

        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except catch_exceptions_types as exp:
                raise exception_type(exp)

        return wrapper

    return decorator
