from __future__ import absolute_import

from mailerlite.response import ApiResponse


class BrandStyles(object):
    # Brand styles base API uri
    base_api_url = "api/brand-styles"

    def __init__(self, api_client):
        self.api_client = api_client

    def get(self):
        """
        Get the brand styles

        Returns the palettes of the account: `brand` (the brand styles of the
        account, or `None` if it has none), `default` and the `presets`.
        Match a palette on its `identifier`, not on its `name`.

        :raises: :class: `ApiError` : API request failed
        :return: JSON object
        :rtype: ApiResponse
        """

        return ApiResponse(self.api_client.request("GET", self.base_api_url))
