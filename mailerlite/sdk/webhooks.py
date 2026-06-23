from __future__ import absolute_import


class Webhooks(object):
    # Webhooks base API uri
    base_api_url = "api/webhooks"

    def __init__(self, api_client):
        self.api_client = api_client

    def list(self):
        """
        Lists all webhooks

        Returns a list of all webhooks.
        Ref: https://developers.mailerlite.com/docs/webhooks.html#list-all-webhooks

        :return: JSON array
        :rtype: dict
        """

        return self.api_client.request("GET", self.base_api_url).json()

    def get(self, webhook_id):
        """
        Get a webhook

        Returns information about single webhook.
        Ref: https://developers.mailerlite.com/docs/webhooks.html#get-a-webhook

        :param webhook_id: int Webhook ID
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(webhook_id, int):
            raise TypeError(
                f"`webhook_id` type is not valid. Expected `int`, got {type(webhook_id)}."
            )

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{webhook_id}"
        ).json()

    def update(self, webhook_id, events=None, url=None, name=None, enabled=True):
        """
        Update a webhook

        Provides ability to update an existing webhook.
        Ref: https://developers.mailerlite.com/docs/webhooks.html#update-a-webhook

        :param webhook_id: int Webhook ID
        :param events: list A list of events https://developers.mailerlite.com/docs/webhooks.html#available-events
        :param url: str Webhook URL
        :param name: str Webhook name
        :param enabled: bool Defines the state of a webhook
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(webhook_id, int):
            raise TypeError(
                f"`webhook_id` type is not valid. Expected `int`, got {type(webhook_id)}."
            )

        if type(events) is not list and events is not None:
            raise TypeError(
                f"`events` type is not valid. Expected `list`, got {type(events)}."
            )

        params = locals()
        body_params = {}
        for key, val in params.items():
            if val is not None and key not in ["self", "webhook_id"]:
                body_params[key] = val

        return self.api_client.request(
            "PUT", f"{self.base_api_url}/{webhook_id}", body=body_params
        ).json()

    def create(self, events, url, name=None):
        """
        Create a webhook

        Provides ability to create a new webhook.
        Ref: https://developers.mailerlite.com/docs/webhooks.html#create-a-webhook

        :param events: list A list of events https://developers.mailerlite.com/docs/webhooks.html#available-events
        :param url: str Webhook URL
        :param name: str Webhook name
        :raises: :class: `TypeError` : `events` type is not valid
        :return: JSON array
        :rtype: dict
        """

        if type(events) is not list:
            raise TypeError(
                f"`events` type is not valid. Expected `list`, got {type(events)}."
            )

        body_params = {"events": events, "url": url}
        if len(name) > 0:
            body_params["name"] = name

        return self.api_client.request(
            "POST", self.base_api_url, body=body_params
        ).json()

    def delete(self, webhook_id):
        """
        Delete a webhook

        Provides ability to delete existing webhook.
        Ref: https://developers.mailerlite.com/docs/webhooks.html#delete-a-webhook

        :param webhook_id: int Webhook URL
        :raises: :class: `TypeError` : `webhook_id` type is not valid
        :return: `true` if action was successful, `false` if form was not found
        :rtype: bool
        """

        if not isinstance(webhook_id, int):
            raise TypeError(
                f"`webhook_id` type is not valid. Expected `int`, got {type(webhook_id)}."
            )

        self.api_client.request("DELETE", f"{self.base_api_url}/{webhook_id}")

        return True
