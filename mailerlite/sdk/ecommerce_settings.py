from __future__ import absolute_import


class EcommerceSettings(object):
    # E-commerce settings base API uri
    base_api_url = "api/ecommerce/settings"

    def __init__(self, api_client):
        self.api_client = api_client

    def get(self):
        """
        Get the e-commerce tracking settings
        Ref: https://developers.mailerlite.com/docs/ecommerce/settings

        :return: JSON array
        :rtype: dict
        """

        return self.api_client.request("GET", self.base_api_url).json()
