def format_query_params(available_params, **kwargs):

    query_params = {}
    for key, val in kwargs.items():
        if key not in available_params:
            raise TypeError("Got an unknown argument '%s'" % key)
        if key == "filter":
            for filter_key, filter_value in val.items():
                query_params[f"filter[{filter_key}]"] = filter_value
        else:
            query_params[key] = val

    return query_params
