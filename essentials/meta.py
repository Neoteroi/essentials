import warnings
from functools import wraps


class DeprecatedException(Exception):
    def __init__(self, param_name):
        super().__init__("Member `%s` is deprecated" % param_name)


def deprecated(message=None, raise_exception=False):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    if message:
        message = " " + message
    else:
        message = ""

    def _deprecated(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            warnings.warn_explicit(
                f"`{f.__name__}` is deprecated.{message}",
                category=DeprecationWarning,
                filename=f.__code__.co_filename,
                lineno=f.__code__.co_firstlineno + 1,
            )
            if raise_exception:
                raise DeprecatedException(f.__name__)
            return f(*args, **kwargs)

        return wrapped

    return _deprecated
