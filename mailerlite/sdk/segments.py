from __future__ import absolute_import


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

        :param **kwargs: dict You can pass additional arguments - page and limit
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON array
        :rtype: dict
        """

        available_params = ["limit", "page"]

        params = locals()
        query_params = {}
        for key, val in params["kwargs"].items():
            if key not in available_params:
                raise TypeError("Got an unknown argument '%s'" % key)
            query_params[key] = val

        return self.api_client.request("GET", self.base_api_url, query_params).json()

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
            query_params[key] = val

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{segment_id}/subscribers", query_params
        ).json()

    def update(self, segment_id, name):
        """
        Update a segment

        Provides ability to update a segment.
        Ref: https://developers.mailerlite.com/docs/segments.html#update-segment

        :param segment_id: int Segment ID
        :param name: str Maximum length of 255 characters
        :raises: :class: `ValueError` : `name` cannot exceed 255 characters
        :raises: :class: `TypeError` : `segment_id` type is not valid
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(segment_id, int):
            raise TypeError(
                f"`segment_id` type is not valid. Expected `int`, got {type(segment_id)}."
            )

        if len(name) > 255:
            raise ValueError("`name` cannot exceed 255 characters.")

        params = locals()
        body_params = {"name": name}

        response = self.api_client.request(
            "PUT", f"{self.base_api_url}/{segment_id}", body=body_params
        )

        return True if response.status_code == 200 else False

    def delete(self, segment_id):
        """
        Delete a segment

        Provides ability to delete a segment.
        Ref: https://developers.mailerlite.com/docs/segments.html#delete-segment

        :param segment_id: int Segment ID
        :raises: :class: `TypeError` : `segment_id` type is not valid
        :return: `true` if action was successful, `false` if form was not found
        :rtype: bool
        """

        if not isinstance(segment_id, int):
            raise TypeError(
                f"`segment_id` type is not valid. Expected `int`, got {type(segment_id)}."
            )

        response = self.api_client.request(
            "DELETE", f"{self.base_api_url}/{segment_id}"
        )

        return True if response.status_code == 204 else False
