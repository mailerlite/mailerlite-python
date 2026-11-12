from __future__ import absolute_import

from mailerlite.sdk.ecommerce_resource import EcommerceResource


class EcommerceImports(EcommerceResource):
    def products(self, shop_id, products):
        """
        Import products
        Ref: https://developers.mailerlite.com/docs/ecommerce/import

        :param shop_id: int Shop ID
        :param products: list The products to import
        :return: JSON array
        :rtype: dict
        """

        if type(products) is not list:
            raise TypeError(
                f"`products` type is not valid. Expected `list`, got {type(products)}."
            )

        return self.api_client.request(
            "POST", self._shop_url(shop_id, "/products/import"), body=products
        ).json()

    def categories(self, shop_id, categories):
        """
        Import categories
        Ref: https://developers.mailerlite.com/docs/ecommerce/import

        :param shop_id: int Shop ID
        :param categories: list The categories to import
        :return: JSON array
        :rtype: dict
        """

        if type(categories) is not list:
            raise TypeError(
                f"`categories` type is not valid. Expected `list`, got {type(categories)}."
            )

        return self.api_client.request(
            "POST", self._shop_url(shop_id, "/categories/import"), body=categories
        ).json()

    def customers(self, shop_id, customers):
        """
        Import customers
        Ref: https://developers.mailerlite.com/docs/ecommerce/import

        :param shop_id: int Shop ID
        :param customers: list The customers to import
        :return: JSON array
        :rtype: dict
        """

        if type(customers) is not list:
            raise TypeError(
                f"`customers` type is not valid. Expected `list`, got {type(customers)}."
            )

        return self.api_client.request(
            "POST", self._shop_url(shop_id, "/customers/import"), body=customers
        ).json()

    def orders(self, shop_id, orders):
        """
        Import orders
        Ref: https://developers.mailerlite.com/docs/ecommerce/import

        :param shop_id: int Shop ID
        :param orders: list The orders to import
        :return: JSON array
        :rtype: dict
        """

        if type(orders) is not list:
            raise TypeError(
                f"`orders` type is not valid. Expected `list`, got {type(orders)}."
            )

        return self.api_client.request(
            "POST", self._shop_url(shop_id, "/orders/import"), body={"orders": orders}
        ).json()
