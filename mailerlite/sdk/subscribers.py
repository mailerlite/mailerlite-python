from __future__ import absolute_import

import re
from urllib.parse import quote

from mailerlite.sdk._request_params import query_params, reject_unknown

_EMAIL_RE = re.compile(r"[\w.]+\@[\w.]+")


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

        :param **kwargs: dict You can pass additional arguments - cursor, page, limit, sort, include, start_date, end_date, with_fields, with_groups or filter by status, group, automation, form, site, page, import or post
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON array
        :rtype: dict
        """

        available_params = [
            "filter",
            "limit",
            "cursor",
            "page",
            "sort",
            "include",
            "start_date",
            "end_date",
            "with_fields",
            "with_groups",
        ]

        return self.api_client.request(
            "GET", self.base_api_url, query_params(kwargs, available_params)
        ).json()

    def create(self, email, **kwargs):
        """
        Create a subscriber

        Provides ability to create a new subscriber.
        Ref: https://developers.mailerlite.com/docs/subscribers.html#create-update-subscriber

        :param email: string Valid email address as per RFC 2821
        :param **kwargs: dict You can pass additional arguments - fields, groups, status, subscribed_at, ip_address, opted_in_at, optin_ip, unsubscribed_at, resubscribe, double_optin and notes. `double_optin` is ignored for normal API tokens; the account setting applies
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
            "resubscribe",
            "double_optin",
            "notes",
        ]

        if not _EMAIL_RE.search(email):
            raise TypeError("`email` is not a valid email address.")

        reject_unknown(kwargs, available_params)
        self._validate_body(kwargs)

        return self.api_client.request(
            "POST", self.base_api_url, body={"email": email, **kwargs}
        ).json()

    def update(self, email, **kwargs):
        """
        Update a subscriber

        Provides ability to update an existing subscriber with `PUT /subscribers/{subscriber}`.
        `groups` replaces the subscriber's groups, so groups that are not listed are removed.
        A missing subscriber returns 404. Use `create` for the additive upsert.
        Ref: https://developers.mailerlite.com/docs/subscribers.html

        :param email: string/int Email address or ID of the subscriber
        :param **kwargs: dict You can pass additional arguments - new_email, fields, groups, status, subscribed_at, ip_address, opted_in_at, optin_ip and unsubscribed_at. `new_email` changes the email address of the subscriber
        :raises: :class: `TypeError` : `email` is not a valid email address
        :raises: :class: `TypeError` : `new_email` is not a valid email address
        :raises: :class: `TypeError` : `fields` argument should be a dict
        :raises: :class: `TypeError` : `groups` argument should be a list
        :raises: :class: `TypeError` : Got an unknown argument
        :raises: :class: `requests.HTTPError` : API request failed, e.g. subscriber was not found
        :return: JSON array
        :rtype: dict
        """

        available_params = [
            "new_email",
            "fields",
            "groups",
            "status",
            "subscribed_at",
            "ip_address",
            "opted_in_at",
            "optin_ip",
            "unsubscribed_at",
        ]

        if not isinstance(email, int) and not _EMAIL_RE.search(email):
            raise TypeError("`email` is not a valid email address.")

        reject_unknown(kwargs, available_params)
        self._validate_body(kwargs)

        body_params = dict(kwargs)
        if "new_email" in body_params:
            new_email = body_params.pop("new_email")
            if not _EMAIL_RE.search(new_email):
                raise TypeError("`new_email` is not a valid email address.")
            body_params["email"] = new_email

        return self.api_client.request(
            "PUT", self._subscriber_path(email), body=body_params
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

        if not isinstance(subscriber_id, int):
            valid = _EMAIL_RE.search(subscriber_id)

            if not valid:
                raise TypeError(
                    "Provided email address or subscriber id are not valid."
                )

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
        :raises: :class: `requests.HTTPError` : API request failed, e.g. subscriber was not found
        :return: `true` if action was successful
        :rtype: bool
        """

        if not isinstance(subscriber_id, int):
            raise TypeError(
                f"`subscriber_id` type is not valid. Expected `int`, got {type(subscriber_id)}."
            )

        self.api_client.request("DELETE", f"{self.base_api_url}/{subscriber_id}")

        return True

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
        :raises: :class: `requests.HTTPError` : API request failed, e.g. subscriber was not found
        :return: `true` if action was successful
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

        self.api_client.request(
            "DELETE", f"{self.base_api_url}/{subscriber_id}/groups/{group_id}"
        )

        return True

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
        :raises: :class: `requests.HTTPError` : API request failed, e.g. subscriber was not found
        :return: `true` if action was successful
        :rtype: bool
        """

        if not isinstance(subscriber_id, int):
            raise TypeError(
                f"`subscriber_id` type is not valid. Expected `int`, got {type(subscriber_id)}."
            )

        self.api_client.request("POST", f"{self.base_api_url}/{subscriber_id}/forget")

        return True

    def activity_log(self, subscriber_id, **kwargs):
        """
        List subscriber activity

        Returns the activity log of a subscriber.
        Ref: https://developers.mailerlite.com/docs/subscribers.html

        :param subscriber_id: int Subscriber ID
        :param **kwargs: dict You can pass additional arguments - limit, page or filter by log_name
        :raises: :class: `TypeError` : `subscriber_id` type is not valid
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(subscriber_id, int):
            raise TypeError(
                f"`subscriber_id` type is not valid. Expected `int`, got {type(subscriber_id)}."
            )

        return self.api_client.request(
            "GET",
            f"{self.base_api_url}/{subscriber_id}/activity-log",
            query_params(kwargs, ["filter", "limit", "page"]),
        ).json()

    def _validate_body(self, kwargs):
        if "fields" in kwargs and type(kwargs["fields"]) is not dict:
            raise TypeError("`fields` argument should be a dict.")

        if "groups" in kwargs and type(kwargs["groups"]) is not list:
            raise TypeError("`groups` argument should be a list.")

    def _subscriber_path(self, email_or_id):
        return f"{self.base_api_url}/{quote(str(email_or_id), safe='@')}"
