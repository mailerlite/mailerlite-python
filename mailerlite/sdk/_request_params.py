from __future__ import absolute_import


def reject_unknown(kwargs, available_params):
    for key in kwargs:
        if key not in available_params:
            raise TypeError("Got an unknown argument '%s'" % key)


def query_value(value):
    if isinstance(value, bool):
        return int(value)

    if isinstance(value, (list, tuple)):
        return ",".join(str(query_value(item)) for item in value)

    return value


def query_params(kwargs, available_params):
    reject_unknown(kwargs, available_params)

    params = {}
    for key, value in kwargs.items():
        if key == "filter":
            for filter_key, filter_value in value.items():
                if filter_value is not None:
                    params[f"filter[{filter_key}]"] = query_value(filter_value)
        elif value is not None:
            params[key] = query_value(value)

    return params


def body_params(kwargs, available_params):
    reject_unknown(kwargs, available_params)

    return kwargs
