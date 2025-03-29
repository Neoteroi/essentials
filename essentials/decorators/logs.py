import logging
from functools import wraps
from inspect import iscoroutinefunction
from logging import Logger
from typing import Callable, Optional, TypeVar
from uuid import uuid4

from essentials.diagnostics import StopWatch

T = TypeVar("T")
IdFactory = Callable[[], str]
FuncType = Callable[..., T]


def _default_id_factory() -> str:
    return str(uuid4())


def log(
    logger: Optional[Logger] = None,
    id_factory: Optional[IdFactory] = None,
    log_arguments: bool = False,
    log_return_value: bool = False,
    level=logging.INFO,
    call_msg="%s; called; call id: %s",
    call_msg_with_input="%s; called; call id: %s; args: %s; kwargs: %s",
    completed_msg="%s; completed; call id: %s; elapsed %s ms",
    completed_msg_with_output="%s; completed; call id: %s; elapsed %s ms; output: %s",
    exc_message="%s; unhandled exception; call id: %s; elapsed %s ms",
) -> Callable[[FuncType], FuncType]:

    if not id_factory:
        id_factory = _default_id_factory

    if logger is None:
        logger = logging.getLogger("fn_calls")

    def before(name, fn, args, kwargs):
        function_call_id = id_factory()
        fn.call_id = function_call_id

        if log_arguments:
            logger.log(level, call_msg_with_input, name, function_call_id, args, kwargs)
        else:
            logger.log(level, call_msg, name, function_call_id)
        return function_call_id

    def on_exception(name, stop_watch, exc, function_call_id):
        stop_watch.stop()
        logger.exception(
            exc_message, name, function_call_id, stop_watch.elapsed_ms, exc_info=exc
        )

    def after(name, stop_watch, function_call_id, value):
        if log_return_value:
            logger.log(
                level,
                completed_msg_with_output,
                name,
                function_call_id,
                stop_watch.elapsed_ms,
                value,
            )
        else:
            logger.log(
                level, completed_msg, name, function_call_id, stop_watch.elapsed_ms
            )

    def log_decorator(fn):
        nonlocal logger
        name = fn.__module__ + "." + fn.__name__

        if iscoroutinefunction(fn):

            @wraps(fn)
            async def async_wrapper(*args, **kwargs):
                function_call_id = before(name, fn, args, kwargs)

                with StopWatch() as stop_watch:
                    try:
                        value = await fn(*args, **kwargs)
                    except Exception as exc:
                        on_exception(name, stop_watch, exc, function_call_id)
                        raise

                after(name, stop_watch, function_call_id, value)
                return value

            return async_wrapper

        @wraps(fn)
        def wrapper(*args, **kwargs):
            function_call_id = before(name, fn, args, kwargs)

            with StopWatch() as stop_watch:
                try:
                    value = fn(*args, **kwargs)
                except Exception as exc:
                    on_exception(name, stop_watch, exc, function_call_id)
                    raise

            after(name, stop_watch, function_call_id, value)
            return value

        return wrapper

    return log_decorator
