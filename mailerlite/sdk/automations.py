from __future__ import absolute_import

from mailerlite.sdk._request_params import body_params, query_params, query_value


class Automations(object):
    # Automations base API uri
    base_api_url = "api/automations"
    templates_api_url = "api/automation-templates"

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

        :param **kwargs: You can pass additional arguments - page, limit, sort, with_steps or to filter by folder, group, enabled, status, name, automation_state and drafts_state
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON array
        :rtype: dict
        """

        params = query_params(kwargs, ["filter", "page", "limit", "sort", "with_steps"])

        return self.api_client.request("GET", self.base_api_url, params).json()

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
        :param: kwargs: You can pass additional arguments - page, limit, sort, with_subscribers or to filter by status, date_from, date_to, scheduled_from, scheduled_to and search. `with_subscribers=True` adds each subscriber's id, email and name
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        with_subscribers = kwargs.pop("with_subscribers", None)
        params = query_params(kwargs, ["filter", "page", "limit", "sort"])
        if with_subscribers:
            params["with_subscribers"] = 1

        return self.api_client.request(
            "GET",
            f"{self.base_api_url}/{automation_id}/activity",
            params,
        ).json()

    def create(self, name):
        """
        Create an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param name: str Automation name
        :return: JSON dict
        """

        return self.api_client.request(
            "POST", self.base_api_url, body={"name": name}
        ).json()

    def update(self, automation_id, name, **kwargs):
        """
        Update an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param name: str Automation name
        :param **kwargs: You can pass additional arguments - trigger_data or triggers
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        body = {"name": name, **body_params(kwargs, ["trigger_data", "triggers"])}

        return self.api_client.request(
            "PUT", f"{self.base_api_url}/{automation_id}", body=body
        ).json()

    def delete(self, automation_id):
        """
        Delete an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :raises: :class: `requests.HTTPError` : API request failed, e.g. automation was not found
        :return: `true` if action was successful
        :rtype: bool
        """

        self.api_client.request("DELETE", f"{self.base_api_url}/{automation_id}")

        return True

    def copy(self, automation_id):
        """
        Copy an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :return: JSON dict
        """

        return self.api_client.request(
            "POST", f"{self.base_api_url}/{automation_id}/copy"
        ).json()

    def enable(self, automation_id):
        """
        Enable an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :return: JSON dict
        """

        return self.api_client.request(
            "POST", f"{self.base_api_url}/{automation_id}/enable"
        ).json()

    def disable(self, automation_id):
        """
        Disable an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :return: JSON dict
        """

        return self.api_client.request(
            "POST", f"{self.base_api_url}/{automation_id}/disable"
        ).json()

    def test(self, automation_id, email):
        """
        Send a test of an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param email: str Address to send the test to
        :raises: :class: `requests.HTTPError` : API request failed
        :return: `true` if action was successful
        :rtype: bool
        """

        self.api_client.request(
            "POST", f"{self.base_api_url}/{automation_id}/test", body={"email": email}
        )

        return True

    def add_subscribers(self, automation_id, **kwargs):
        """
        Add subscribers to an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param **kwargs: You can pass additional arguments - step_id, emails or groups
        :raises: :class: `TypeError` : Got an unknown argument
        :raises: :class: `requests.HTTPError` : API request failed
        :return: `true` if action was successful
        :rtype: bool
        """

        body = body_params(kwargs, ["step_id", "emails", "groups"])

        self.api_client.request(
            "POST",
            f"{self.base_api_url}/{automation_id}/add-subscribers",
            body=body,
        )

        return True

    def readd(self, automation_id, readd_subscribers_to, filter, **kwargs):
        """
        Re-add subscribers to an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param readd_subscribers_to: str last_completed_step, last_failed_step or selected_step
        :param filter: dict Selects which runs to re-add
        :param **kwargs: You can pass additional arguments - selected_step_id
        :raises: :class: `TypeError` : Got an unknown argument
        :raises: :class: `requests.HTTPError` : API request failed
        :return: `true` if action was successful
        :rtype: bool
        """

        body = {
            "readd_subscribers_to": readd_subscribers_to,
            "filter": filter,
            **body_params(kwargs, ["selected_step_id"]),
        }

        self.api_client.request(
            "POST", f"{self.base_api_url}/{automation_id}/readd", body=body
        )

        return True

    def activity_add_to_group(self, automation_id, destination_groups, filter):
        """
        Copy automation subscribers to groups
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param destination_groups: list Group IDs to copy the subscribers into
        :param filter: dict Selects which runs to copy subscribers from
        :raises: :class: `requests.HTTPError` : API request failed
        :return: `true` if action was successful
        :rtype: bool
        """

        self.api_client.request(
            "POST",
            f"{self.base_api_url}/{automation_id}/activity/add-to-group",
            body={"destination_groups": destination_groups, "filter": filter},
        )

        return True

    def activity_cancel_automation(self, automation_id, filter):
        """
        Cancel active automation runs
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param filter: dict Selects which active runs to cancel
        :raises: :class: `requests.HTTPError` : API request failed
        :return: `true` if action was successful
        :rtype: bool
        """

        self.api_client.request(
            "POST",
            f"{self.base_api_url}/{automation_id}/activity/cancel-automation",
            body={"filter": filter},
        )

        return True

    def activity_skip_delay(self, automation_id, filter):
        """
        Skip the delay of active automation runs
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param filter: dict Selects which active runs skip their delay
        :raises: :class: `requests.HTTPError` : API request failed
        :return: `true` if action was successful
        :rtype: bool
        """

        self.api_client.request(
            "POST",
            f"{self.base_api_url}/{automation_id}/activity/skip-delay",
            body={"filter": filter},
        )

        return True

    def list_triggers(self, automation_id):
        """
        List the triggers of an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{automation_id}/triggers"
        ).json()

    def create_trigger(self, automation_id, type, **kwargs):
        """
        Create an automation trigger
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param type: str Trigger type
        :param **kwargs: You can pass additional arguments - data
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        body = {"type": type, **body_params(kwargs, ["data"])}

        return self.api_client.request(
            "POST", f"{self.base_api_url}/{automation_id}/triggers", body=body
        ).json()

    def get_trigger(self, automation_id, trigger_id):
        """
        Get an automation trigger
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param trigger_id: Trigger ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{automation_id}/triggers/{trigger_id}"
        ).json()

    def update_trigger(self, automation_id, trigger_id, **kwargs):
        """
        Update an automation trigger
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param trigger_id: Trigger ID
        :param **kwargs: You can pass additional arguments - data
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        return self.api_client.request(
            "PUT",
            f"{self.base_api_url}/{automation_id}/triggers/{trigger_id}",
            body=body_params(kwargs, ["data"]),
        ).json()

    def delete_trigger(self, automation_id, trigger_id):
        """
        Delete an automation trigger
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param trigger_id: Trigger ID
        :raises: :class: `requests.HTTPError` : API request failed, e.g. trigger was not found
        :return: `true` if action was successful
        :rtype: bool
        """

        self.api_client.request(
            "DELETE", f"{self.base_api_url}/{automation_id}/triggers/{trigger_id}"
        )

        return True

    def list_steps(self, automation_id):
        """
        List the steps of an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{automation_id}/steps/index"
        ).json()

    def create_step(self, automation_id, type, **kwargs):
        """
        Create an automation step
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param type: str Step type
        :param **kwargs: You can pass additional arguments - parent_id, branch, move_to_branch or data
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        body = {
            "type": type,
            **body_params(kwargs, ["parent_id", "branch", "move_to_branch", "data"]),
        }

        return self.api_client.request(
            "POST", f"{self.base_api_url}/{automation_id}/steps", body=body
        ).json()

    def get_step(self, automation_id, step_id):
        """
        Get an automation step
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param step_id: Step ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{automation_id}/steps/{step_id}"
        ).json()

    def update_step(self, automation_id, step_id, **kwargs):
        """
        Update an automation step
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param step_id: Step ID
        :param **kwargs: You can pass additional arguments - parent_id, data or reschedule_waiting_subscribers
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        body = body_params(
            kwargs, ["parent_id", "data", "reschedule_waiting_subscribers"]
        )

        return self.api_client.request(
            "PUT",
            f"{self.base_api_url}/{automation_id}/steps/{step_id}",
            body=body,
        ).json()

    def delete_step(self, automation_id, step_id, **kwargs):
        """
        Delete an automation step
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param step_id: Step ID
        :param **kwargs: You can pass additional arguments - branch_to_delete
        :raises: :class: `TypeError` : Got an unknown argument
        :raises: :class: `requests.HTTPError` : API request failed, e.g. step was not found
        :return: `true` if action was successful
        :rtype: bool
        """

        self.api_client.request(
            "DELETE",
            f"{self.base_api_url}/{automation_id}/steps/{step_id}",
            query_params(kwargs, ["branch_to_delete"]),
        )

        return True

    def copy_step(self, automation_id, step_id, **kwargs):
        """
        Copy an automation step
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param step_id: Step ID
        :param **kwargs: You can pass additional arguments - parent_id, branch or move_to_branch
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        body = body_params(kwargs, ["parent_id", "branch", "move_to_branch"])

        return self.api_client.request(
            "POST",
            f"{self.base_api_url}/{automation_id}/steps/{step_id}/copy",
            body=body,
        ).json()

    def reorder_steps(self, automation_id, dragged_step_id, **kwargs):
        """
        Move an automation step
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param dragged_step_id: Step ID of the step to move
        :param **kwargs: You can pass additional arguments - new_parent_step_id, branch or branch_for_child
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        body = {
            "dragged_step_id": dragged_step_id,
            **body_params(kwargs, ["new_parent_step_id", "branch", "branch_for_child"]),
        }

        return self.api_client.request(
            "POST",
            f"{self.base_api_url}/{automation_id}/steps/reorder",
            body=body,
        ).json()

    def select_ab_test_winner(self, automation_id, step_id, ab_test_winner):
        """
        Select the winner of an A/B test step
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param step_id: Step ID
        :param ab_test_winner: str a_path, b_path or c_path
        :return: JSON dict
        """

        return self.api_client.request(
            "PUT",
            f"{self.base_api_url}/{automation_id}/steps/{step_id}/select-ab-test-winner",
            body={"ab_test_winner": ab_test_winner},
        ).json()

    def get_email_content(self, automation_id, email_id):
        """
        Get the HTML content of an automation email
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param email_id: Email ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{automation_id}/emails/{email_id}/content"
        ).json()

    def update_email_content(self, automation_id, email_id, html):
        """
        Update the HTML content of an automation email
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param email_id: Email ID
        :param html: str HTML content of the email
        :return: JSON dict
        """

        return self.api_client.request(
            "PUT",
            f"{self.base_api_url}/{automation_id}/emails/{email_id}/content",
            body={"html": html},
        ).json()

    def email_report_stats(self, automation_id, email_id, **kwargs):
        """
        Get the report stats of an automation email
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param email_id: Email ID
        :param **kwargs: You can pass additional arguments - start_date, end_date, shop_id or excel
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        return self.api_client.request(
            "GET",
            f"{self.base_api_url}/{automation_id}/emails/{email_id}/report-stats",
            query_params(kwargs, ["start_date", "end_date", "shop_id", "excel"]),
        ).json()

    def email_unsubscribe_reasons(self, automation_id, email_id):
        """
        Get the unsubscribe reasons of an automation email
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param email_id: Email ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET",
            f"{self.base_api_url}/{automation_id}/emails/{email_id}/unsubscribe-reasons",
        ).json()

    def list_templates(self, **kwargs):
        """
        List automation templates
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param **kwargs: You can pass additional arguments - page, limit or to filter by type and category
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        return self.api_client.request(
            "GET",
            self.templates_api_url,
            query_params(kwargs, ["filter", "page", "limit"]),
        ).json()

    def select_template(self, template_id):
        """
        Create an automation from a template
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param template_id: Automation template ID
        :return: JSON dict
        """

        return self.api_client.request(
            "POST", f"{self.base_api_url}/select-template/{template_id}"
        ).json()

    def steps_run_counts(self, automation_id):
        """
        Get the run counts of all steps of an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{automation_id}/steps/run-counts"
        ).json()

    def step_run_counts(self, automation_id, step_id):
        """
        Get the run counts of one automation step
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param step_id: Step ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{automation_id}/steps/run-counts/{step_id}"
        ).json()

    def triggers_run_counts(self, automation_id):
        """
        Get the run counts of all triggers of an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{automation_id}/triggers/run-counts"
        ).json()

    def trigger_run_counts(self, automation_id, trigger_id):
        """
        Get the run counts of one automation trigger
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param trigger_id: Trigger ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET",
            f"{self.base_api_url}/{automation_id}/triggers/run-counts/{trigger_id}",
        ).json()

    def ab_steps_stats(self, automation_id):
        """
        Get the stats of all A/B test steps of an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{automation_id}/ab-steps-stats"
        ).json()

    def ab_step_stats(self, automation_id, step_id):
        """
        Get the stats of one A/B test step
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param step_id: Step ID
        :return: JSON dict
        """

        return self.api_client.request(
            "GET", f"{self.base_api_url}/{automation_id}/ab-steps-stats/{step_id}"
        ).json()

    def step_subscribers(self, automation_id, step_id, status, **kwargs):
        """
        List the subscribers on an automation step
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param step_id: Step ID
        :param status: str queued or completed
        :param **kwargs: You can pass additional arguments - page, limit, sort or to filter by date_from, date_to, search and id
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        return self._activity_subscribers(
            automation_id, "steps", step_id, status, kwargs
        )

    def trigger_subscribers(self, automation_id, trigger_id, status, **kwargs):
        """
        List the subscribers on an automation trigger
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param trigger_id: Trigger ID
        :param status: str queued or completed
        :param **kwargs: You can pass additional arguments - page, limit, sort or to filter by date_from, date_to, search and id
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        return self._activity_subscribers(
            automation_id, "triggers", trigger_id, status, kwargs
        )

    def email_monthly_totals(self, automation_id, **kwargs):
        """
        Get the monthly email totals of an automation
        Ref: https://developers.mailerlite.com/docs/automations.html

        :param automation_id: Automation ID
        :param **kwargs: You can pass additional arguments - start_date, end_date, shop_id or excel
        :raises: :class: `TypeError` : Got an unknown argument
        :return: JSON dict
        """

        return self.api_client.request(
            "GET",
            f"{self.base_api_url}/{automation_id}/monthly-totals/email",
            query_params(kwargs, ["start_date", "end_date", "shop_id", "excel"]),
        ).json()

    def _activity_subscribers(self, automation_id, kind, item_id, status, kwargs):
        params = {
            "status": query_value(status),
            **query_params(kwargs, ["filter", "page", "limit", "sort"]),
        }

        return self.api_client.request(
            "GET",
            f"{self.base_api_url}/{automation_id}/activity/{kind}/{item_id}/subscribers",
            params,
        ).json()
