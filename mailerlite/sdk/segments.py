from __future__ import absolute_import

from mailerlite.sdk._request_params import body_params, query_params


class Segments(object):
    # Segments base API uri
    base_api_url = "api/segments"

    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **kwargs):
        """
        Lists all segments

        Returns a list of all segments.
        Ref: https://developers.mailerlite.com/docs/segments.html#list-all-segments

        :param **kwargs: dict You can pass additional arguments - page, limit and sort
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON array
        :rtype: dict
        """

        return self.api_client.request(
            "GET", self.base_api_url, query_params(kwargs, ["limit", "page", "sort"])
        ).json()

    def get(self, segment_id, **kwargs):
        """
        Get a segment

        Returns information about a segment.
        Ref: https://developers.mailerlite.com/docs/segments.html#get-subscribers-belonging-to-a-segment

        :param segment_id: int Segment ID
        :param **kwargs: dict You can pass additional arguments - after, limit or filter by status
        :raises: :class: `TypeError` : Got an unknown argument
        :raises: :class: `TypeError` : `segment_id` type is not valid
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(segment_id, int):
            raise TypeError(
                f"`segment_id` type is not valid. Expected `int`, got {type(segment_id)}."
            )

        if not isinstance(segment_id, int):
            raise TypeError("Segment ID are not valid.")

        available_params = ["filter", "limit", "after"]

        params = locals()
        query_params = {}
        for key, val in params["kwargs"].items():
            if key not in available_params:
                raise TypeError("Got an unknown argument '%s'" % key)
            if key == "filter":
                for filter_key, filter_value in val.items():
                    query_params[f"filter[{filter_key}]"] = filter_value
            else:
                query_params[key] = val

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{segment_id}", query_params
        ).json()

    def get_subscribers(self, segment_id, **kwargs):
        """
        Get subscribers belonging to a segment

        Returns a list of subscribers belonging to a segment.
        Ref: https://developers.mailerlite.com/docs/segments.html#get-subscribers-belonging-to-a-segment

        :param segment_id: int Segment ID
        :param **kwargs: dict You can pass additional arguments - cursor, limit or filter by status. `after` is deprecated, use `cursor`
        :raises: :class: `TypeError` : Got an unknown argument
        :raises: :class: `TypeError` : `segment_id` type is not valid
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(segment_id, int):
            raise TypeError(
                f"`segment_id` type is not valid. Expected `int`, got {type(segment_id)}."
            )

        if not isinstance(segment_id, int):
            raise TypeError("Segment ID are not valid.")

        return self.api_client.request(
            "GET",
            f"{self.base_api_url}/{segment_id}/subscribers",
            query_params(kwargs, ["filter", "limit", "cursor", "after"]),
        ).json()

    def update(self, segment_id, name, **kwargs):
        """
        Update a segment

        Provides ability to update a segment.
        Ref: https://developers.mailerlite.com/docs/segments.html#update-segment

        :param segment_id: int Segment ID
        :param name: str Maximum length of 255 characters
        :param **kwargs: dict You can pass additional arguments - filter
        :raises: :class: `ValueError` : `name` cannot exceed 255 characters
        :raises: :class: `TypeError` : `segment_id` type is not valid
        :raises: :class: `TypeError` : Got an unknown argument
        :raises: :class: `requests.HTTPError` : API request failed, e.g. segment was not found
        :return: `true` if action was successful
        :rtype: bool
        """

        if not isinstance(segment_id, int):
            raise TypeError(
                f"`segment_id` type is not valid. Expected `int`, got {type(segment_id)}."
            )

        if len(name) > 255:
            raise ValueError("`name` cannot exceed 255 characters.")

        body = {"name": name, **body_params(kwargs, ["filter"])}

        self.api_client.request("PUT", f"{self.base_api_url}/{segment_id}", body=body)

        return True

    def delete(self, segment_id):
        """
        Delete a segment

        Provides ability to delete a segment.
        Ref: https://developers.mailerlite.com/docs/segments.html#delete-segment

        :param segment_id: int Segment ID
        :raises: :class: `TypeError` : `segment_id` type is not valid
        :raises: :class: `requests.HTTPError` : API request failed, e.g. segment was not found
        :return: `true` if action was successful
        :rtype: bool
        """

        if not isinstance(segment_id, int):
            raise TypeError(
                f"`segment_id` type is not valid. Expected `int`, got {type(segment_id)}."
            )

        self.api_client.request("DELETE", f"{self.base_api_url}/{segment_id}")

        return True
