from __future__ import absolute_import


class Campaigns(object):
    # Campaigns base API uri
    base_api_url = "api/campaigns"

    def __init__(self, api_client):
        self.api_client = api_client

    def create(self, campaign):
        """
        Create a campaign
        Ref: https://developers.mailerlite.com/docs/campaigns.html#create-a-campaign

        :param campaign: dict A dict that contains all campaign related arguments
        :return: JSON array
        :rtype: dict
        """

        return self.api_client.request("POST", self.base_api_url, body=campaign).json()

    def update(self, campaign_id, campaign):
        """
        Update campaign

        Provides ability to update single campaign.
        Ref: https://developers.mailerlite.com/docs/campaigns.html#update-campaign

        :param campaign_id: int Id of the campaign
        :param campaign: dict A dict that contains all campaign related arguments
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(campaign_id, int):
            raise TypeError(
                f"`campaign_id` type is not valid. Expected `int`, got {type(campaign_id)}."
            )

        return self.api_client.request(
            "PUT", f"{self.base_api_url}/{campaign_id}", body=campaign
        ).json()

    def get(self, campaign_id):
        """
        Get a campaign

        Returns information about single campaign.
        Ref: https://developers.mailerlite.com/docs/campaigns.html#get-a-campaign

        :param campaign_id: int Id of the campaign
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(campaign_id, int):
            raise TypeError(
                f"`campaign_id` type is not valid. Expected `int`, got {type(campaign_id)}."
            )

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{campaign_id}"
        ).json()

    def list(self, **kwargs):
        """
        Campaign list

        Returns a list of all campaigns.
        Ref: https://developers.mailerlite.com/docs/campaigns.html#campaign-list

        :param **kwargs: dict Allows you to pass additional arguments as query params (filter, limit and page)
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

    def schedule(self, campaign_id, schedule):
        """
        Schedule a campaign

        Provides with ability to schedule existing campaign.
        Ref: https://developers.mailerlite.com/docs/campaigns.html#schedule-a-campaign

        :param campaign_id: int Id of the campaign
        :param schedule: dict A dict with relevant parametes for scheduling campaign
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(campaign_id, int):
            raise TypeError(
                f"`campaign_id` type is not valid. Expected `int`, got {type(campaign_id)}."
            )

        return self.api_client.request(
            "POST",
            f"{self.base_api_url}/{campaign_id}/schedule",
            body=schedule,
        ).json()

    def cancel(self, campaign_id):
        """
        Cancel a ready campaign

        Provides with ability to cancel a campaign that is currently in a ready state.
        Ref: https://developers.mailerlite.com/docs/campaigns.html#cancel-a-ready-campaign

        :param campaign_id: int Id of the campaign
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(campaign_id, int):
            raise TypeError(
                f"`campaign_id` type is not valid. Expected `int`, got {type(campaign_id)}."
            )

        return self.api_client.request(
            "POST", f"{self.base_api_url}/{campaign_id}/cancel"
        ).json()

    def delete(self, campaign_id):
        """
        Delete a campaign

        Provides with ability to delete existing campaign.
        Ref: https://developers.mailerlite.com/docs/campaigns.html#delete-a-campaign

        :param campaign_id: int Id of the campaign
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(campaign_id, int):
            raise TypeError(
                f"`campaign_id` type is not valid. Expected `int`, got {type(campaign_id)}."
            )

        response = self.api_client.request(
            "DELETE", f"{self.base_api_url}/{campaign_id}"
        )

        return True if response.status_code == 204 else False

    def activity(self, campaign_id):
        """
        Get subscribers' activity of a sent campaign

        Returns subscribers' activity of a campaign.
        Ref: https://developers.mailerlite.com/docs/campaigns.html#get-subscribers-activity-of-a-sent-campaign

        :param campaign_id: int Id of the campaign
        :return: JSON array
        :rtype: dict
        """

        if not isinstance(campaign_id, int):
            raise TypeError(
                f"`campaign_id` type is not valid. Expected `int`, got {type(campaign_id)}."
            )

        return self.api_client.request(
            "POST", f"{self.base_api_url}/{campaign_id}/reports/subscriber-activity"
        ).json()

    def languages(self):
        """
        Campaign languages

        Returns a list of all campaign languages available.
        Ref: https://developers.mailerlite.com/docs/campaign-languages.html#response

        :return: JSON array
        :rtype: dict
        """

        return self.api_client.request("GET", f"{self.base_api_url}/languages").json()
