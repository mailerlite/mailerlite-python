from __future__ import absolute_import

from mailerlite.sdk.ecommerce_resource import EcommerceResource


class EcommerceShops(EcommerceResource):
    def list(self, **kwargs):
        """
        List shops
        Ref: https://developers.mailerlite.com/docs/ecommerce/shops

        :param **kwargs: You can pass additional arguments - page or limit
        :return: JSON array
        :rtype: dict
        """

        query_params = self._query_params(kwargs, ["page", "limit"])

        return self.api_client.request("GET", self.base_api_url, query_params).json()

    def get(self, shop_id):
        """
        Get a shop
        Ref: https://developers.mailerlite.com/docs/ecommerce/shops

        :param shop_id: int Shop ID
        :return: JSON array
        :rtype: dict
        """

        return self.api_client.request("GET", self._shop_url(shop_id)).json()

    def create(self, name, url, currency, **kwargs):
        """
        Create a shop
        Ref: https://developers.mailerlite.com/docs/ecommerce/shops

        :param name: str Shop name
        :param url: str Shop URL
        :param currency: str ISO 4217 currency code, e.g. EUR
        :param **kwargs: Any other shop fields, e.g. platform, group_id, enabled
        :return: JSON array
        :rtype: dict
        """

        body_params = {"name": name, "url": url, "currency": currency, **kwargs}

        return self.api_client.request(
            "POST", self.base_api_url, body=body_params
        ).json()

    def update(self, shop_id, **kwargs):
        """
        Update a shop
        Ref: https://developers.mailerlite.com/docs/ecommerce/shops

        :param shop_id: int Shop ID
        :param **kwargs: The shop fields to update
        :return: JSON array
        :rtype: dict
        """

        return self.api_client.request(
            "PUT", self._shop_url(shop_id), body=kwargs
        ).json()

    def delete(self, shop_id):
        """
        Delete a shop
        Ref: https://developers.mailerlite.com/docs/ecommerce/shops

        :param shop_id: int Shop ID
        :return: `true` if action was successful
        :rtype: bool
        """

        self.api_client.request("DELETE", self._shop_url(shop_id))

        return True

    def stats(self, shop_id, start_date, end_date):
        """
        Get a shop's attributed orders and revenue over a period of up to one year
        Ref: https://developers.mailerlite.com/docs/ecommerce/shops

        :param shop_id: int Shop ID
        :param start_date: str First day, e.g. 2026-01-01
        :param end_date: str Last day, included
        :return: JSON array
        :rtype: dict
        """

        return self.api_client.request(
            "GET",
            self._shop_url(shop_id, "/reports/stats"),
            {"start_date": start_date, "end_date": end_date},
        ).json()
