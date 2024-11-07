import asyncio
import time
from functools import wraps
from inspect import iscoroutinefunction
from typing import Callable, Optional, Tuple, Type, TypeVar, Union

T = TypeVar("T")
FuncType = Callable[..., T]
CatchException = Union[Tuple[Type[Exception]], Type[Exception], None]
OnException = Optional[Callable[[Type[Exception], int], None]]


def _get_retry_async_wrapper(
    fn: FuncType,
    times: int,
    delay: float,
    catch_exceptions_types: CatchException,
    on_exception: OnException,
    loop,
) -> FuncType:
    @wraps(fn)
    async def async_wrapper(*args, **kwargs):
        attempt = 0

        while True:
            try:
                return await fn(*args, **kwargs)
            except catch_exceptions_types as ex:
                attempt += 1
                if on_exception:
                    if iscoroutinefunction(on_exception):
                        await on_exception(ex, attempt)
                    else:
                        on_exception(ex, attempt)

                if attempt > times:
                    raise

                if delay is not None:
                    await asyncio.sleep(delay)

    return async_wrapper


def retry(
    times: int = 3,
    delay: Optional[float] = 0.1,
    catch_exceptions_types: CatchException = None,
    on_exception: OnException = None,
    loop=None,
) -> Callable[[FuncType], FuncType]:
    if catch_exceptions_types is None:
        catch_exceptions_types = Exception

    def retry_decorator(fn):
        if iscoroutinefunction(fn):
            return _get_retry_async_wrapper(
                fn, times, delay, catch_exceptions_types, on_exception, loop
            )

        @wraps(fn)
        def wrapper(*args, **kwargs):
            attempt = 0

            while True:
                try:
                    return fn(*args, **kwargs)
                except catch_exceptions_types as ex:
                    attempt += 1
                    if on_exception:
                        on_exception(ex, attempt)

                    if attempt > times:
                        raise

                    if delay is not None:
                        time.sleep(delay)

        return wrapper

    return retry_decorator
