from __future__ import absolute_import

from mailerlite.sdk.ecommerce_resource import EcommerceResource


class EcommerceOrders(EcommerceResource):
    def list(self, shop_id, **kwargs):
        """
        List orders
        Ref: https://developers.mailerlite.com/docs/ecommerce/orders

        :param shop_id: int Shop ID
        :param **kwargs: You can pass additional arguments - page, limit, sort, filter
        :return: JSON array
        :rtype: dict
        """

        query_params = self._query_params(kwargs, ["page", "limit", "sort", "filter"])

        return self.api_client.request(
            "GET", self._shop_url(shop_id, "/orders"), query_params
        ).json()

    def get(self, shop_id, order_id):
        """
        Get a order
        Ref: https://developers.mailerlite.com/docs/ecommerce/orders

        :param shop_id: int Shop ID
        :param order_id: int Order ID
        :return: JSON array
        :rtype: dict
        """

        self._check_id("order_id", order_id)

        return self.api_client.request(
            "GET", self._shop_url(shop_id, f"/orders/{order_id}")
        ).json()

    def create(self, shop_id, customer, cart, **kwargs):
        """
        Create or update a order
        Ref: https://developers.mailerlite.com/docs/ecommerce/orders

        :param shop_id: int Shop ID
        :param **kwargs: Any other order fields
        :return: JSON array
        :rtype: dict
        """

        body_params = {"customer": customer, "cart": cart, **kwargs}

        return self.api_client.request(
            "POST", self._shop_url(shop_id, "/orders"), body=body_params
        ).json()

    def update(self, shop_id, order_id, **kwargs):
        """
        Update a order
        Ref: https://developers.mailerlite.com/docs/ecommerce/orders

        :param shop_id: int Shop ID
        :param order_id: int Order ID
        :param **kwargs: The order fields to update
        :return: JSON array
        :rtype: dict
        """

        self._check_id("order_id", order_id)

        return self.api_client.request(
            "PUT", self._shop_url(shop_id, f"/orders/{order_id}"), body=kwargs
        ).json()

    def delete(self, shop_id, order_id):
        """
        Delete a order
        Ref: https://developers.mailerlite.com/docs/ecommerce/orders

        :param shop_id: int Shop ID
        :param order_id: int Order ID
        :return: `true` if action was successful
        :rtype: bool
        """

        self._check_id("order_id", order_id)

        self.api_client.request(
            "DELETE", self._shop_url(shop_id, f"/orders/{order_id}")
        )

        return True
