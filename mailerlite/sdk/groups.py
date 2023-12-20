from __future__ import absolute_import


class Groups(object):
    # Groups base API uri
    base_api_url = "api/groups"

    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **kwargs):
        """
        Lists all groups

        Returns a list of all groups.
        Ref: https://developers.mailerlite.com/docs/groups.html#list-all-groups

        :param **kwargs: You can pass additional arguments - page, limit, sort or to filter by name
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON array
        :rtype: dict
        """

        available_params = ["list", "limit", "page", "sort", "filter"]

        params = locals()
        query_params = {}
        for key, val in params["kwargs"].items():
            if key not in available_params:
                raise TypeError("Got an unknown argument '%s'" % key)
            if key == "filter":
                for filter_key, filter_value in val.items():
                    query_params[filter_key] = filter_value
            else:
                query_params[key] = val

        return self.api_client.request("GET", self.base_api_url, query_params).json()

    def create(self, name):
        """
        Create a group

        Provides an ability to create a new group.
        Ref: https://developers.mailerlite.com/docs/groups.html#create-a-group

        :param name: str Maximum length of 255 characters
        :raises: :class: `ValueError` : `name` cannot exceed 255 characters
        :return: JSON array
        :rtype: dict
        """

        if len(name) > 255:
            raise ValueError("`name` cannot exceed 255 characters.")

        params = locals()
        body_params = {"name": name}

        return self.api_client.request(
            "POST", self.base_api_url, body=body_params
        ).json()

    def update(self, group_id, name):
        """
        Update a group

        Provides an ability to update a group.
        Ref: https://developers.mailerlite.com/docs/groups.html#update-a-group

        :param group_id: int Group ID
        :param name: str Maximum length of 255 characters
        :raises: :class: `ValueError` : `name` cannot exceed 255 characters
        :raises: :class: `TypeError` : `group_id` type is not valid
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(group_id, int):
            raise TypeError(
                f"`group_id` type is not valid. Expected `int`, got {type(group_id)}."
            )

        if len(name) > 255:
            raise ValueError("Group name cannot exceed 255 characters.")

        params = locals()
        body_params = {"name": name}

        return self.api_client.request(
            "PUT", f"{self.base_api_url}/{group_id}", body=body_params
        ).json()

    def delete(self, group_id):
        """
        Delete a group

        Provides an ability to delete a group.
        Ref: https://developers.mailerlite.com/docs/groups.html#delete-group

        :param group_id: int Group ID
        :raises: :class: `TypeError` : `group_id` type is not valid
        :return: `true` if action was successful, `false` if form was not found
        :rtype: bool
        """

        if not isinstance(group_id, int):
            raise TypeError(
                f"`group_id` type is not valid. Expected `int`, got {type(group_id)}."
            )

        response = self.api_client.request("DELETE", f"{self.base_api_url}/{group_id}")

        return True if response.status_code == 204 else False

    def get_group_subscribers(self, group_id, **kwargs):
        """
        Get subscribers belonging to a group

        Returns a list of all subscribers belonging to a group.
        Ref: https://developers.mailerlite.com/docs/groups.html#get-subscribers-belonging-to-a-group

        :param group_id: int Group ID
        :param **kwargs: You can pass additional arguments - page, limit, sort or to filter by status
        :raises: :class: `TypeError` : Got an unknown argument
        :raises: :class: `TypeError` : `group_id` type is not valid
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(group_id, int):
            raise TypeError(
                f"`group_id` type is not valid. Expected `int`, got {type(group_id)}."
            )

        available_params = ["filter", "limit", "page"]

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
            "GET",
            f"{self.base_api_url}/{group_id}/subscribers",
            query_params,
        ).json()
