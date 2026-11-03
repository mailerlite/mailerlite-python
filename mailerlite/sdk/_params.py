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


def reject_unknown(kwargs, available_params):
    for key in kwargs:
        if key not in available_params:
            raise TypeError("Got an unknown argument '%s'" % key)


def query_value(value):
    """A query string value: booleans as 1/0, lists comma-joined"""

    if isinstance(value, bool):
        return int(value)

    if isinstance(value, (list, tuple)):
        return ",".join(str(query_value(item)) for item in value)

    return value


def filter_params(filter):
    if filter is None:
        return {}

    require_dict(filter, "filter")

    return {
        f"filter[{key}]": query_value(value)
        for key, value in without_none(filter).items()
    }


def query_params(kwargs, available_params):
    """The query string of a method with **kwargs. `None` values are not sent."""

    reject_unknown(kwargs, available_params)

    params = {}
    for key, value in kwargs.items():
        if key == "filter":
            params.update(filter_params(value))
        elif value is not None:
            params[key] = query_value(value)

    return params


def body_params(kwargs, available_params):
    """The JSON body of a method with **kwargs. `None` values are not sent."""

    reject_unknown(kwargs, available_params)

    return without_none(kwargs)


def idempotency_headers(key):
    if key is None:
        return None

    return {"Idempotency-Key": key}
