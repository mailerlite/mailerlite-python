from __future__ import absolute_import

from mailerlite.sdk.ecommerce_resource import EcommerceResource


class EcommerceCategories(EcommerceResource):
    def list(self, shop_id, **kwargs):
        """
        List categories
        Ref: https://developers.mailerlite.com/docs/ecommerce/categories

        :param shop_id: int Shop ID
        :param **kwargs: You can pass additional arguments - page, limit, filter
        :return: JSON array
        :rtype: dict
        """

        query_params = self._query_params(kwargs, ["page", "limit", "filter"])

        return self.api_client.request(
            "GET", self._shop_url(shop_id, "/categories"), query_params
        ).json()

    def get(self, shop_id, category_id):
        """
        Get a category
        Ref: https://developers.mailerlite.com/docs/ecommerce/categories

        :param shop_id: int Shop ID
        :param category_id: int Category ID
        :return: JSON array
        :rtype: dict
        """

        self._check_id("category_id", category_id)

        return self.api_client.request(
            "GET", self._shop_url(shop_id, f"/categories/{category_id}")
        ).json()

    def create(self, shop_id, name, **kwargs):
        """
        Create or update a category
        Ref: https://developers.mailerlite.com/docs/ecommerce/categories

        :param shop_id: int Shop ID
        :param **kwargs: Any other category fields
        :return: JSON array
        :rtype: dict
        """

        body_params = {"name": name, **kwargs}

        return self.api_client.request(
            "POST", self._shop_url(shop_id, "/categories"), body=body_params
        ).json()

    def update(self, shop_id, category_id, **kwargs):
        """
        Update a category
        Ref: https://developers.mailerlite.com/docs/ecommerce/categories

        :param shop_id: int Shop ID
        :param category_id: int Category ID
        :param **kwargs: The category fields to update
        :return: JSON array
        :rtype: dict
        """

        self._check_id("category_id", category_id)

        return self.api_client.request(
            "PUT", self._shop_url(shop_id, f"/categories/{category_id}"), body=kwargs
        ).json()

    def delete(self, shop_id, category_id):
        """
        Delete a category
        Ref: https://developers.mailerlite.com/docs/ecommerce/categories

        :param shop_id: int Shop ID
        :param category_id: int Category ID
        :return: `true` if action was successful
        :rtype: bool
        """

        self._check_id("category_id", category_id)

        self.api_client.request(
            "DELETE", self._shop_url(shop_id, f"/categories/{category_id}")
        )

        return True

    def products(self, shop_id, category_id, **kwargs):
        """
        List the products in a category
        Ref: https://developers.mailerlite.com/docs/ecommerce/categories-products

        :param shop_id: int Shop ID
        :param category_id: int Category ID
        :param **kwargs: You can pass additional arguments - page or limit
        :return: JSON array
        :rtype: dict
        """

        self._check_id("category_id", category_id)
        query_params = self._query_params(kwargs, ["page", "limit"])

        return self.api_client.request(
            "GET",
            self._shop_url(shop_id, f"/categories/{category_id}/products"),
            query_params,
        ).json()

    def assign_product(self, shop_id, category_id, product_id):
        """
        Assign a product to a category
        Ref: https://developers.mailerlite.com/docs/ecommerce/categories-products

        :param shop_id: int Shop ID
        :param category_id: int Category ID
        :param product_id: int Product ID
        :return: JSON array
        :rtype: dict
        """

        self._check_id("category_id", category_id)
        self._check_id("product_id", product_id)

        return self.api_client.request(
            "PUT",
            self._shop_url(shop_id, f"/categories/{category_id}/products/{product_id}"),
            body={},
        ).json()

    def unassign_product(self, shop_id, category_id, product_id):
        """
        Unassign a product from a category
        Ref: https://developers.mailerlite.com/docs/ecommerce/categories-products

        :param shop_id: int Shop ID
        :param category_id: int Category ID
        :param product_id: int Product ID
        :return: `true` if action was successful
        :rtype: bool
        """

        self._check_id("category_id", category_id)
        self._check_id("product_id", product_id)

        self.api_client.request(
            "DELETE",
            self._shop_url(shop_id, f"/categories/{category_id}/products/{product_id}"),
        )

        return True
