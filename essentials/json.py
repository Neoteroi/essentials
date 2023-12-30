"""
This module defines a user-friendly json encoder,
supporting time objects, UUID and bytes.
"""
import base64
import dataclasses
import json
from datetime import date, datetime, time
from enum import Enum
from uuid import UUID
from decimal import Decimal

__all__ = ["FriendlyEncoder", "dumps"]


class FriendlyEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            if hasattr(obj, "dict"):
                return obj.dict()
            if isinstance(obj, time):
                return obj.strftime("%H:%M:%S")
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, date):
                return obj.strftime("%Y-%m-%d")
            if isinstance(obj, bytes):
                return base64.urlsafe_b64encode(obj).decode("utf8")
            if isinstance(obj, UUID):
                return str(obj)
            if isinstance(obj, Decimal):
                return str(obj)
            if isinstance(obj, Enum):
                return obj.value
            if dataclasses.is_dataclass(obj):
                return dataclasses.asdict(obj)
            raise


def dumps(
    obj,
    skipkeys=False,
    ensure_ascii=False,
    check_circular=True,
    allow_nan=True,
    cls=None,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
    **kw,
):
    if cls is None:
        cls = FriendlyEncoder
    return json.dumps(
        obj,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=cls,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
        **kw,
    )
