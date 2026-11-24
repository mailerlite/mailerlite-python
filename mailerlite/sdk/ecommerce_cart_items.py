from __future__ import absolute_import

from mailerlite.sdk.ecommerce_resource import EcommerceResource


class EcommerceCartItems(EcommerceResource):
    def _items_url(self, shop_id, cart_id, path=""):
        self._check_id("cart_id", cart_id)

        return self._shop_url(shop_id, f"/carts/{cart_id}/items{path}")

    def list(self, shop_id, cart_id, **kwargs):
        """
        List a cart's items
        Ref: https://developers.mailerlite.com/docs/ecommerce/cart-items

        :param shop_id: int Shop ID
        :param cart_id: int Cart ID
        :param **kwargs: You can pass additional arguments - page or limit
        :return: JSON array
        :rtype: dict
        """

        query_params = self._query_params(kwargs, ["page", "limit"])

        return self.api_client.request(
            "GET", self._items_url(shop_id, cart_id), query_params
        ).json()

    def get(self, shop_id, cart_id, item_id):
        """
        Get a cart item
        Ref: https://developers.mailerlite.com/docs/ecommerce/cart-items

        :param shop_id: int Shop ID
        :param cart_id: int Cart ID
        :param item_id: int Cart item ID
        :return: JSON array
        :rtype: dict
        """

        self._check_id("item_id", item_id)

        return self.api_client.request(
            "GET", self._items_url(shop_id, cart_id, f"/{item_id}")
        ).json()

    def create(self, shop_id, cart_id, **kwargs):
        """
        Add an item to a cart
        Ref: https://developers.mailerlite.com/docs/ecommerce/cart-items

        :param shop_id: int Shop ID
        :param cart_id: int Cart ID
        :param **kwargs: The cart item fields, e.g. ecommerce_product_id, quantity
        :return: JSON array
        :rtype: dict
        """

        return self.api_client.request(
            "POST", self._items_url(shop_id, cart_id), body=kwargs
        ).json()

    def update(self, shop_id, cart_id, item_id, **kwargs):
        """
        Update a cart item
        Ref: https://developers.mailerlite.com/docs/ecommerce/cart-items

        :param shop_id: int Shop ID
        :param cart_id: int Cart ID
        :param item_id: int Cart item ID
        :param **kwargs: The cart item fields to update
        :return: JSON array
        :rtype: dict
        """

        self._check_id("item_id", item_id)

        return self.api_client.request(
            "PUT", self._items_url(shop_id, cart_id, f"/{item_id}"), body=kwargs
        ).json()

    def delete(self, shop_id, cart_id, item_id):
        """
        Delete a cart item
        Ref: https://developers.mailerlite.com/docs/ecommerce/cart-items

        :param shop_id: int Shop ID
        :param cart_id: int Cart ID
        :param item_id: int Cart item ID
        :return: `true` if action was successful
        :rtype: bool
        """

        self._check_id("item_id", item_id)

        self.api_client.request(
            "DELETE", self._items_url(shop_id, cart_id, f"/{item_id}")
        )

        return True
