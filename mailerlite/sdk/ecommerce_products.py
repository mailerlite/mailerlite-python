from __future__ import absolute_import

from mailerlite.sdk.ecommerce_resource import EcommerceResource


class EcommerceProducts(EcommerceResource):
    def list(self, shop_id, **kwargs):
        """
        List products
        Ref: https://developers.mailerlite.com/docs/ecommerce/products

        :param shop_id: int Shop ID
        :param **kwargs: You can pass additional arguments - page, limit, sort, filter
        :return: JSON array
        :rtype: dict
        """

        query_params = self._query_params(kwargs, ["page", "limit", "sort", "filter"])

        return self.api_client.request(
            "GET", self._shop_url(shop_id, "/products"), query_params
        ).json()

    def get(self, shop_id, product_id):
        """
        Get a product
        Ref: https://developers.mailerlite.com/docs/ecommerce/products

        :param shop_id: int Shop ID
        :param product_id: int Product ID
        :return: JSON array
        :rtype: dict
        """

        self._check_id("product_id", product_id)

        return self.api_client.request(
            "GET", self._shop_url(shop_id, f"/products/{product_id}")
        ).json()

    def create(self, shop_id, name, **kwargs):
        """
        Create or update a product
        Ref: https://developers.mailerlite.com/docs/ecommerce/products

        :param shop_id: int Shop ID
        :param **kwargs: Any other product fields
        :return: JSON array
        :rtype: dict
        """

        body_params = {"name": name, **kwargs}

        return self.api_client.request(
            "POST", self._shop_url(shop_id, "/products"), body=body_params
        ).json()

    def update(self, shop_id, product_id, **kwargs):
        """
        Update a product
        Ref: https://developers.mailerlite.com/docs/ecommerce/products

        :param shop_id: int Shop ID
        :param product_id: int Product ID
        :param **kwargs: The product fields to update
        :return: JSON array
        :rtype: dict
        """

        self._check_id("product_id", product_id)

        return self.api_client.request(
            "PUT", self._shop_url(shop_id, f"/products/{product_id}"), body=kwargs
        ).json()

    def delete(self, shop_id, product_id):
        """
        Delete a product
        Ref: https://developers.mailerlite.com/docs/ecommerce/products

        :param shop_id: int Shop ID
        :param product_id: int Product ID
        :return: `true` if action was successful
        :rtype: bool
        """

        self._check_id("product_id", product_id)

        self.api_client.request(
            "DELETE", self._shop_url(shop_id, f"/products/{product_id}")
        )

        return True

    def change_status(self, shop_id, product_id, enabled):
        """
        Enable or disable a product
        Ref: https://developers.mailerlite.com/docs/ecommerce/products

        :param shop_id: int Shop ID
        :param product_id: int Product ID
        :param enabled: bool Whether the product is enabled
        :return: JSON array
        :rtype: dict
        """

        self._check_id("product_id", product_id)

        return self.api_client.request(
            "PUT",
            self._shop_url(shop_id, f"/products/{product_id}/change-status"),
            body={"status": enabled},
        ).json()

    def assign_categories(self, shop_id, product_id, categories, replace=False):
        """
        Assign categories to a product
        Ref: https://developers.mailerlite.com/docs/ecommerce/products

        :param shop_id: int Shop ID
        :param product_id: int Product ID
        :param categories: list Category IDs
        :param replace: bool Also remove the categories that are not listed
        :return: JSON array
        :rtype: dict
        """

        self._check_id("product_id", product_id)

        if type(categories) is not list:
            raise TypeError(
                f"`categories` type is not valid. Expected `list`, got {type(categories)}."
            )

        return self.api_client.request(
            "PUT",
            self._shop_url(shop_id, f"/products/{product_id}/categories/multiple"),
            body={"categories": categories, "replace": replace},
        ).json()
