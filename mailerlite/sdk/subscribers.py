from __future__ import absolute_import

import re


class Subscribers(object):
    # Subscribers base API uri
    base_api_url = "api/subscribers"

    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **kwargs):
        """
        Lists all subscribers

        Returns a list of all subscribers.
        Ref: https://developers.mailerlite.com/docs/subscribers.html#list-all-subscribers

        :param **kwargs: dict You can pass additional arguments - page, limit or filter by status
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON array
        :rtype: dict
        """

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

        return self.api_client.request("GET", self.base_api_url, query_params).json()

    def create(self, email, **kwargs):
        """
        Create a subscriber

        Provides ability to create a new subscriber.
        Ref: https://developers.mailerlite.com/docs/subscribers.html#create-update-subscriber

        :param email: string Valid email address as per RFC 2821
        :param **kwargs: dict You can pass additional arguments - fields, groups, status, subscribed_at, ip_address, opted_in_at, optin_ip and unsubscribed_at
        :raises: :class: `TypeError` : `email` is not a valid email address
        :raises: :class: `TypeError` : `fields` argument should be a dict
        :raises: :class: `TypeError` : `groups` argument should be a list
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON array
        :rtype: dict
        """

        available_params = [
            "fields",
            "groups",
            "status",
            "subscribed_at",
            "ip_address",
            "opted_in_at",
            "optin_ip",
            "unsubscribed_at",
        ]

        valid = re.search(r"[\w.]+\@[\w.]+", email)

        if not valid:
            raise TypeError("`email` is not a valid email address.")

        params = locals()
        body_params = {"email": email}

        for key, val in params["kwargs"].items():
            if key not in available_params:
                raise TypeError("Got an unknown argument '%s'" % key)

            if key == "fields" and type(val) is not dict:
                raise TypeError("`fields` argument should be a dict.")

            if key == "groups" and type(val) is not list:
                raise TypeError("`groups` argument should be a list.")

            body_params[key] = val

        return self.api_client.request(
            "POST", self.base_api_url, body=body_params
        ).json()

    def update(self, email, **kwargs):
        """
        Update a subscriber

        Provides ability to update an existing subscriber.
        Ref: https://developers.mailerlite.com/docs/subscribers.html#create-update-subscriber

        :param email: string Valid email address as per RFC 2821
        :param **kwargs: dict You can pass additional arguments - fields, groups, status, subscribed_at, ip_address, opted_in_at, optin_ip and unsubscribed_at
        :raises: :class: `TypeError` : `email` is not a valid email address
        :raises: :class: `TypeError` : `fields` argument should be a dict
        :raises: :class: `TypeError` : `groups` argument should be a list
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON array
        :rtype: dict
        """

        available_params = [
            "fields",
            "groups",
            "status",
            "subscribed_at",
            "ip_address",
            "opted_in_at",
            "optin_ip",
            "unsubscribed_at",
        ]

        valid = re.search(r"[\w.]+\@[\w.]+", email)

        if not valid:
            raise TypeError("`email` is not a valid email address.")

        params = locals()
        body_params = {"email": email}

        for key, val in params["kwargs"].items():
            if key not in available_params:
                raise TypeError("Got an unknown argument '%s'" % key)

            if key == "fields" and type(val) is not dict:
                raise TypeError("`fields` argument should be a dict.")

            if key == "groups" and type(val) is not list:
                raise TypeError("`groups` argument should be a list.")

            body_params[key] = val

        return self.api_client.request(
            "POST", self.base_api_url, body=body_params
        ).json()

    def get(self, subscriber_id):
        """
        Get a subscriber

        Returns information about subscriber.
        Ref: https://developers.mailerlite.com/docs/subscribers.html#fetch-a-subscriber

        :param subscriber_id: int/string Susbscriber email address or ID
        :raises: :class: `TypeError` : Provided email address or subscriber id are not valid
        :return: JSON array
        :rtype: dict
        """

        valid = re.search(r"[\w.]+\@[\w.]+", subscriber_id)

        if not valid and not isinstance(subscriber_id, int):
            raise TypeError("Provided email address or subscriber id are not valid.")

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{subscriber_id}"
        ).json()

    def delete(self, subscriber_id):
        """
        Delete a subscriber

        Provides ability to delete existing subscriber.
        Ref: https://developers.mailerlite.com/docs/subscribers.html#delete-a-subscriber

        :param subscriber_id: int Susbscriber ID
        :raises: :class: `TypeError` : `subscriber_id` type is not valid
        :return: `true` if action was successful, `false` if subscriber was not found
        :rtype: bool
        """

        if not isinstance(subscriber_id, int):
            raise TypeError(
                f"`subscriber_id` type is not valid. Expected `int`, got {type(subscriber_id)}."
            )

        response = self.api_client.request(
            "DELETE", f"{self.base_api_url}/{subscriber_id}"
        )

        return response.status_code

    def get_import(self, import_id):
        """
        Get single import

        Returns a single import report.
        Ref: https://developers.mailerlite.com/docs/subscribers.html#get-single-import

        :param import_id: int Import ID
        :raises: :class: `TypeError` : `import_id` type is not valid
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(import_id, int):
            raise TypeError(
                f"`import_id` type is not valid. Expected `int`, got {type(import_id)}."
            )

        return self.api_client.request(
            "GET", f"{self.base_api_url}/import/{import_id}"
        ).json()

    def assign_subscriber_to_group(self, subscriber_id, group_id):
        """
        Assign subscriber to a group

        Provides the ability to assign an existing subscriber to a group.
        Ref: https://developers.mailerlite.com/docs/groups.html#assign-subscriber-to-a-group

        :param subscriber_id: int Subscriber ID
        :param group_id: int Group ID
        :raises: :class: `TypeError` : `subscriber_id` type is not valid
        :raises: :class: `TypeError` : `group_id` type is not valid
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(subscriber_id, int):
            raise TypeError(
                f"`subscriber_id` type is not valid. Expected `int`, got {type(subscriber_id)}."
            )

        if not isinstance(group_id, int):
            raise TypeError(
                f"`group_id` type is not valid. Expected `int`, got {type(group_id)}."
            )

        return self.api_client.request(
            "POST", f"{self.base_api_url}/{subscriber_id}/groups/{group_id}"
        ).json()

    def unassign_subscriber_from_group(self, subscriber_id, group_id):
        """
        Unassign subscriber to a group

        Provides the ability to unassign an existing subscriber to a group.
        Ref: https://developers.mailerlite.com/docs/groups.html#unassign-subscriber-from-a-group

        :param subscriber_id: int Subscriber ID
        :param group_id: int Group ID
        :raises: :class: `TypeError` : `subscriber_id` type is not valid
        :raises: :class: `TypeError` : `group_id` type is not valid
        :return: `true` if action was successful, `false` if subscriber was not found
        :rtype: bool
        """

        if not isinstance(subscriber_id, int):
            raise TypeError(
                f"`subscriber_id` type is not valid. Expected `int`, got {type(subscriber_id)}."
            )

        if not isinstance(group_id, int):
            raise TypeError(
                f"`group_id` type is not valid. Expected `int`, got {type(group_id)}."
            )

        response = self.api_client.request(
            "DELETE", f"{self.base_api_url}/{subscriber_id}/groups/{group_id}"
        )

        return True if response.status_code == 204 else False

    def count(self):
        """
        Fetch total subscribers count

        Returns a total count of subscribers.
        Ref: https://developers.mailerlite.com/docs/subscribers.html#fetch-total-subscribers-count

        :return: JSON array
        :rtype: dict
        """

        return self.list(limit=0)

    def forget(self, subscriber_id):
        """
        Forget a subscriber

        It will removes the subscriber from your account and all information will be completely deleted in 30 days. This feature is GDPR compliant.If you want to forget a subscriber, send this POST request.
        Ref: https://developers.mailerlite.com/docs/subscribers.html#forget-a-subscriber

        :param subscriber_id: int Susbscriber ID
        :raises: :class: `TypeError` : `subscriber_id` type is not valid
        :return: `true` if action was successful, `false` if subscriber was not found
        :rtype: bool
        """

        if not isinstance(subscriber_id, int):
            raise TypeError(
                f"`subscriber_id` type is not valid. Expected `int`, got {type(subscriber_id)}."
            )

        response = self.api_client.request(
            "POST", f"{self.base_api_url}/{subscriber_id}/forget"
        )

        return response.status_code
