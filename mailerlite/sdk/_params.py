from __future__ import absolute_import

import re

from mailerlite.exceptions import (
    EmptyEtagError,
    EmptyIdError,
    InvalidIdempotencyKeyError,
    InvalidIdError,
)

_ID_PATTERN = re.compile(r"[0-9]+")
# The API accepts 1 to 255 printable ASCII characters
_IDEMPOTENCY_KEY_PATTERN = re.compile(r"[\x20-\x7E]{1,255}")


def path_id(value, name):
    if value is None or value == "":
        raise EmptyIdError(f"`{name}` must not be empty.")

    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise TypeError(
            f"`{name}` type is not valid. Expected `str` or `int`, got {type(value)}."
        )

    value = str(value)
    # fullmatch, because `$` also matches before a final new line,
    # and str.isdigit() also accepts digits that are not ASCII.
    if not _ID_PATTERN.fullmatch(value):
        raise InvalidIdError(f"`{name}` must contain only digits, got {value!r}.")

    return value


def etag(value):
    if value is None or value == "":
        raise EmptyEtagError("`etag` must not be empty.")

    if not isinstance(value, str):
        raise TypeError(f"`etag` type is not valid. Expected `str`, got {type(value)}.")

    return value


def require_dict(value, name):
    if not isinstance(value, dict):
        raise TypeError(
            f"`{name}` type is not valid. Expected `dict`, got {type(value)}."
        )


def without_none(params):
    return {key: value for key, value in params.items() if value is not None}


def filter_params(filter):
    if filter is None:
        return {}

    require_dict(filter, "filter")

    return {f"filter[{key}]": value for key, value in filter.items()}


def idempotency_headers(key):
    if key is None:
        return None

    if not isinstance(key, str):
        raise TypeError(
            f"`idempotency_key` type is not valid. Expected `str`, got {type(key)}."
        )

    # HTTP removes spaces at the start and the end of a header value,
    # so such a key does not reach the API as it is.
    if not _IDEMPOTENCY_KEY_PATTERN.fullmatch(key) or key != key.strip(" "):
        raise InvalidIdempotencyKeyError(
            "`idempotency_key` must be 1 to 255 printable ASCII characters, "
            "without a space at the start or the end."
        )

    return {"Idempotency-Key": key}
