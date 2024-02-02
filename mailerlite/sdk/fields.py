from __future__ import absolute_import


class Fields(object):
    # Fields base API uri
    base_api_url = "api/fields"

    def __init__(self, api_client):
        self.api_client = api_client

    def create(self, name, type):
        """
        Create a field

        Provides ability to createa field.
        Ref: https://developers.mailerlite.com/docs/fields.html#create-a-field

        :param name: string Field name. Maximum length of 255 characters.
        :param type: string Can be text, number or date.
        :raises: :class: `ValueError` : Type be text, number or date
        :raises: :class: `ValueError` : `name` cannot exceed 255 characters
        :return: JSON array
        :rtype: dict
        """

        allowed_types = ["text", "number", "date"]

        if type not in allowed_types:
            raise ValueError("`type` can be text, number or date.")

        if len(name) > 255:
            raise ValueError("`name` cannot exceed 255 characters.")

        body_params = {"name": name, "type": type}

        return self.api_client.request(
            "POST", self.base_api_url, body=body_params
        ).json()

    def list(self, **kwargs):
        """
        List all fields

        Returns a list of all fields.
        Ref: https://developers.mailerlite.com/docs/fields.html#list-all-fields

        :param **kwargs: dict You can pass additional arguments such as `list`, `page`, `filter` and `sort.
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON array
        :rtype: dict
        """

        available_params = ["limit", "page", "filter", "sort"]

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

        return self.api_client.request("GET", self.base_api_url, query_params).json()

    def update(self, field_id, name):
        """
        Update a field

        Provides the ability to update a field.
        Ref: https://developers.mailerlite.com/docs/fields.html#update-a-field

        :param field_id: int Field ID.
        :param name: string Can be text, number or date.
        :raises: :class: `ValueError` : `name` cannot exceed 255 characters
        :raises: :class: `TypeError` : `field_id` type is not valid
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(field_id, int):
            raise TypeError(
                f"`field_id` type is not valid. Expected `int`, got {type(field_id)}."
            )

        if len(name) > 255:
            raise ValueError("Field name cannot exceed 255 characters.")

        body_params = {"name": name}

        return self.api_client.request(
            "PUT", f"{self.base_api_url}/{field_id}", body=body_params
        ).json()

    def delete(self, field_id):
        """
        Delete a field

        Provides the ability to delete a field.
        Ref: https://developers.mailerlite.com/docs/fields.html#update-a-field

        :param field_id: int Field ID.
        :return: `true` if action was successful, `false` if field was not found
        :rtype: bool
        """

        response = self.api_client.request("DELETE", f"{self.base_api_url}/{field_id}")

        return True if response.status_code == 204 else False
