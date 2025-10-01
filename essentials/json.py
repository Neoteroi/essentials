"""
This module defines a user-friendly json encoder,
supporting time objects, UUID and bytes.
"""

import base64
import dataclasses
import json
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import UUID

__all__ = ["FriendlyEncoder", "dumps"]


class FriendlyEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            # The ordering prioritizes the most frequently encountered types first,
            # which should provide better performance in typical use cases.

            # Most common datetime objects first
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, date):
                return obj.strftime("%Y-%m-%d")
            if isinstance(obj, time):
                return obj.strftime("%H:%M:%S")

            # Very common built-in types
            if isinstance(obj, UUID):
                return str(obj)
            if isinstance(obj, Enum):
                return obj.value
            if isinstance(obj, Decimal):
                return str(obj)

            # Common serializable objects
            if dataclasses.is_dataclass(obj):
                return dataclasses.asdict(obj)  # type:ignore[arg-type]
            if hasattr(obj, "model_dump"):  # Pydantic v2
                return obj.model_dump()
            if hasattr(obj, "dict"):  # Pydantic v1 or similar
                return obj.dict()

            # Less common types
            if isinstance(obj, timedelta):
                return obj.total_seconds()
            if isinstance(obj, bytes):
                return base64.urlsafe_b64encode(obj).decode("utf8")
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
) -> str:
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
