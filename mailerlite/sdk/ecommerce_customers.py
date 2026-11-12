from __future__ import absolute_import

from mailerlite.sdk.ecommerce_resource import EcommerceResource


class EcommerceCustomers(EcommerceResource):
    def list(self, shop_id, **kwargs):
        """
        List customers
        Ref: https://developers.mailerlite.com/docs/ecommerce/customers

        :param shop_id: int Shop ID
        :param **kwargs: You can pass additional arguments - page, limit, sort, filter
        :return: JSON array
        :rtype: dict
        """

        query_params = self._query_params(kwargs, ["page", "limit", "sort", "filter"])

        return self.api_client.request(
            "GET", self._shop_url(shop_id, "/customers"), query_params
        ).json()

    def get(self, shop_id, customer_id):
        """
        Get a customer
        Ref: https://developers.mailerlite.com/docs/ecommerce/customers

        :param shop_id: int Shop ID
        :param customer_id: int Customer ID
        :return: JSON array
        :rtype: dict
        """

        self._check_id("customer_id", customer_id)

        return self.api_client.request(
            "GET", self._shop_url(shop_id, f"/customers/{customer_id}")
        ).json()

    def create(self, shop_id, email, **kwargs):
        """
        Create or update a customer
        Ref: https://developers.mailerlite.com/docs/ecommerce/customers

        :param shop_id: int Shop ID
        :param **kwargs: Any other customer fields
        :return: JSON array
        :rtype: dict
        """

        body_params = {"email": email, **kwargs}

        return self.api_client.request(
            "POST", self._shop_url(shop_id, "/customers"), body=body_params
        ).json()

    def update(self, shop_id, customer_id, **kwargs):
        """
        Update a customer
        Ref: https://developers.mailerlite.com/docs/ecommerce/customers

        :param shop_id: int Shop ID
        :param customer_id: int Customer ID
        :param **kwargs: The customer fields to update
        :return: JSON array
        :rtype: dict
        """

        self._check_id("customer_id", customer_id)

        return self.api_client.request(
            "PUT", self._shop_url(shop_id, f"/customers/{customer_id}"), body=kwargs
        ).json()

    def delete(self, shop_id, customer_id):
        """
        Delete a customer
        Ref: https://developers.mailerlite.com/docs/ecommerce/customers

        :param shop_id: int Shop ID
        :param customer_id: int Customer ID
        :return: `true` if action was successful
        :rtype: bool
        """

        self._check_id("customer_id", customer_id)

        self.api_client.request(
            "DELETE", self._shop_url(shop_id, f"/customers/{customer_id}")
        )

        return True
