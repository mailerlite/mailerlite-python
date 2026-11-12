from __future__ import absolute_import


class EcommerceResource(object):
    # E-commerce base API uri
    base_api_url = "api/ecommerce/shops"

    def __init__(self, api_client):
        self.api_client = api_client

    def _shop_url(self, shop_id, path=""):
        self._check_id("shop_id", shop_id)

        return f"{self.base_api_url}/{shop_id}{path}"

    @staticmethod
    def _check_id(name, value):
        if not isinstance(value, int):
            raise TypeError(
                f"`{name}` type is not valid. Expected `int`, got {type(value)}."
            )

    @staticmethod
    def _query_params(kwargs, available_params):
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
