from __future__ import absolute_import

import re

from mailerlite.exceptions import EmptyIdError, InvalidIdError

_ID_PATTERN = re.compile(r"[0-9]+")


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

    return {"Idempotency-Key": key}
