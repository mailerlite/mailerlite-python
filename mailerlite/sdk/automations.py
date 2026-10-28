from __future__ import absolute_import


class Automations(object):
    # Automations base API uri
    base_api_url = "api/automations"

    def __init__(self, api_client):
        """
        Class constructor

        :param api_client: object
        """
        self.api_client = api_client

    def list(self, **kwargs):
        """
        Lists all automations on account
        Ref: https://developers.mailerlite.com/docs/automations.html#list-all-automations

        :param **kwargs: You can pass additional arguments - page, limit or to filter by status, name and group
        :return: JSON array
        :rtype: dict
        """

        available_params = ["filter", "page", "limit"]

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

    def get(self, automation_id):
        """
        Returns information about single automation
        Ref: https://developers.mailerlite.com/docs/automations.html#get-an-automation

        :param: automation_id: Automation ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{automation_id}"
        ).json()

    def activity(self, automation_id, **kwargs):
        """
        Get the subscriber activity for an automation
        Ref: https://developers.mailerlite.com/docs/automations.html#get-the-subscriber-activity-for-an-automation

        :param: automation_id: Automation ID
        :param: kwargs: You can pass additional arguments - page, limit or to filter by status, date_from, date_to
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        available_params = ["filter", "page", "limit"]

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
            f"{self.base_api_url}/{automation_id}/activity",
            query_params,
        ).json()

    def ecommerce_stats(self, automation_id, **kwargs):
        """
        Get the orders and revenue an automation earned
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: int Automation ID
        :param **kwargs: You can pass additional arguments - shop_id, start_date or end_date
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(automation_id, int):
            raise TypeError(
                f"`automation_id` type is not valid. Expected `int`, got {type(automation_id)}."
            )

        query_params = {}
        for key, val in kwargs.items():
            if key not in ["shop_id", "start_date", "end_date"]:
                raise TypeError("Got an unknown argument '%s'" % key)
            query_params[key] = val

        return self.api_client.request(
            "GET",
            f"{self.base_api_url}/{automation_id}/monthly-totals/ecommerce",
            query_params,
        ).json()

    def email_ecommerce_stats(self, automation_id, email_id, **kwargs):
        """
        Get the orders and revenue one automation email earned
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: int Automation ID
        :param email_id: int Email ID
        :param **kwargs: You can pass additional arguments - shop_id, start_date or end_date
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(automation_id, int):
            raise TypeError(
                f"`automation_id` type is not valid. Expected `int`, got {type(automation_id)}."
            )

        if not isinstance(email_id, int):
            raise TypeError(
                f"`email_id` type is not valid. Expected `int`, got {type(email_id)}."
            )

        query_params = {}
        for key, val in kwargs.items():
            if key not in ["shop_id", "start_date", "end_date"]:
                raise TypeError("Got an unknown argument '%s'" % key)
            query_params[key] = val

        return self.api_client.request(
            "GET",
            f"{self.base_api_url}/{automation_id}/emails/{email_id}/ecommerce-overview-stats",
            query_params,
        ).json()

    def ecommerce_orders(self, automation_id, time_frame, **kwargs):
        """
        List the orders attributed to an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: int Automation ID
        :param time_frame: str week, month, two_months, three_months, six_months, year, last_year, all_time or custom
        :param **kwargs: You can pass additional arguments - time_frame_start, time_frame_end, ecommerce_shop_id, page or limit
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(automation_id, int):
            raise TypeError(
                f"`automation_id` type is not valid. Expected `int`, got {type(automation_id)}."
            )

        available_params = [
            "time_frame_start",
            "time_frame_end",
            "ecommerce_shop_id",
            "page",
            "limit",
        ]
        query_params = {"time_frame": time_frame}
        for key, val in kwargs.items():
            if key not in available_params:
                raise TypeError("Got an unknown argument '%s'" % key)
            query_params[key] = val

        return self.api_client.request(
            "GET",
            f"{self.base_api_url}/{automation_id}/order-activity",
            query_params,
        ).json()
