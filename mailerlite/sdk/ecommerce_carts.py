from __future__ import absolute_import

from mailerlite.sdk.ecommerce_resource import EcommerceResource


class EcommerceCarts(EcommerceResource):
    def list(self, shop_id, **kwargs):
        """
        List carts
        Ref: https://developers.mailerlite.com/docs/ecommerce/cart

        :param shop_id: int Shop ID
        :param **kwargs: You can pass additional arguments - page or limit
        :return: JSON array
        :rtype: dict
        """

        query_params = self._query_params(kwargs, ["page", "limit"])

        return self.api_client.request(
            "GET", self._shop_url(shop_id, "/carts"), query_params
        ).json()

    def get(self, shop_id, cart_id):
        """
        Get a cart
        Ref: https://developers.mailerlite.com/docs/ecommerce/cart

        :param shop_id: int Shop ID
        :param cart_id: int Cart ID
        :return: JSON array
        :rtype: dict
        """

        self._check_id("cart_id", cart_id)

        return self.api_client.request(
            "GET", self._shop_url(shop_id, f"/carts/{cart_id}")
        ).json()

    def update(self, shop_id, cart_id, **kwargs):
        """
        Update a cart
        Ref: https://developers.mailerlite.com/docs/ecommerce/cart

        :param shop_id: int Shop ID
        :param cart_id: int Cart ID
        :param **kwargs: The cart fields to update, e.g. checkout_url, cart_total
        :return: JSON array
        :rtype: dict
        """

        self._check_id("cart_id", cart_id)

        return self.api_client.request(
            "PUT", self._shop_url(shop_id, f"/carts/{cart_id}"), body=kwargs
        ).json()
