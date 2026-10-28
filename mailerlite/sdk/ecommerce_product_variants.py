from __future__ import absolute_import

from mailerlite.sdk.ecommerce_resource import EcommerceResource


class EcommerceProductVariants(EcommerceResource):
    def list(self, shop_id, product_id):
        """
        List a product's variants
        Ref: https://developers.mailerlite.com/docs/ecommerce/product-variants

        :param shop_id: int Shop ID
        :param product_id: int Product ID
        :return: JSON array
        :rtype: dict
        """

        self._check_id("product_id", product_id)

        return self.api_client.request(
            "GET", self._shop_url(shop_id, f"/products/{product_id}/variants")
        ).json()

    def sync(self, shop_id, product_id, variants):
        """
        Create or update a product's variants from a list
        Ref: https://developers.mailerlite.com/docs/ecommerce/product-variants

        :param shop_id: int Shop ID
        :param product_id: int Product ID
        :param variants: list Variants, each with at least name and attributes
        :return: JSON array
        :rtype: dict
        """

        self._check_id("product_id", product_id)

        if type(variants) is not list:
            raise TypeError(
                f"`variants` type is not valid. Expected `list`, got {type(variants)}."
            )

        return self.api_client.request(
            "POST",
            self._shop_url(shop_id, f"/products/{product_id}/variants"),
            body=variants,
        ).json()

    def update(self, shop_id, product_id, variant_id, name, attributes, **kwargs):
        """
        Update a product variant
        Ref: https://developers.mailerlite.com/docs/ecommerce/product-variants

        :param shop_id: int Shop ID
        :param product_id: int Product ID
        :param variant_id: int Variant ID
        :param name: str Variant name
        :param attributes: dict Attributes that define the variant, e.g. {"size": "L"}
        :param **kwargs: Any other variant fields, e.g. price_type, price
        :return: JSON array
        :rtype: dict
        """

        self._check_id("product_id", product_id)
        self._check_id("variant_id", variant_id)

        body_params = {"name": name, "attributes": attributes, **kwargs}

        return self.api_client.request(
            "PUT",
            self._shop_url(shop_id, f"/products/{product_id}/variants/{variant_id}"),
            body=body_params,
        ).json()

    def delete(self, shop_id, product_id, variant_id):
        """
        Delete a product variant
        Ref: https://developers.mailerlite.com/docs/ecommerce/product-variants

        :param shop_id: int Shop ID
        :param product_id: int Product ID
        :param variant_id: int Variant ID
        :return: `true` if action was successful
        :rtype: bool
        """

        self._check_id("product_id", product_id)
        self._check_id("variant_id", variant_id)

        self.api_client.request(
            "DELETE",
            self._shop_url(shop_id, f"/products/{product_id}/variants/{variant_id}"),
        )

        return True
