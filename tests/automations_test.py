import os

import mailerlite as MailerLite
import pytest
import vcr
from dotenv import load_dotenv
from pytest import fixture


@fixture
def automation_keys():
    return [
        "id",
        "name",
        "enabled",
        "trigger_data",
        "steps",
        "triggers",
        "complete",
        "broken",
        "warnings",
        "stats",
    ]


class TestAutomations:
    # Automationd ID used in tests
    automation_id = 112078014094771336

    @classmethod
    def setup_class(self):
        load_dotenv()

        self.client = MailerLite.Client({"api_key": os.getenv("API_KEY")})

    def test_api_url_is_properly_set(self):
        assert self.client.automations.base_api_url == "api/automations"

    @vcr.use_cassette(
        "tests/vcr_cassettes/automations-list.yml", filter_headers=["Authorization"]
    )
    def test_list_of_all_automations_should_be_returned(self, automation_keys):
        response = self.client.automations.list()

        assert isinstance(response, dict)
        assert isinstance(response["data"], list)
        assert isinstance(response["data"][0], dict)
        assert set(automation_keys).issubset(response["data"][0].keys())

    @vcr.use_cassette(
        "tests/vcr_cassettes/automations-get.yml", filter_headers=["Authorization"]
    )
    def test_automation_information_should_be_returned_when_valid_automation_id_is_provided(
        self, automation_keys
    ):
        response = self.client.automations.get(self.automation_id)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(automation_keys).issubset(response["data"].keys())

    @vcr.use_cassette(
        "tests/vcr_cassettes/automations-activity.yml", filter_headers=["Authorization"]
    )
    def test_automation_activity_information_should_be_returned_when_valid_automation_id_is_provided(
        self,
    ):
        response = self.client.automations.activity(
            self.automation_id, filter={"status": "active"}
        )

        assert isinstance(response, dict)
        assert isinstance(response["data"], list)


def _method_ids(cases):
    return [case[0] for case in cases]


REQUEST_CASES = [
    (
        "list",
        [],
        {
            "filter": {"enabled": True, "automation_state": "workflows"},
            "page": 2,
            "limit": 10,
            "sort": "-created_at",
            "with_steps": True,
        },
        "GET",
        "/automations",
        {
            "filter[enabled]": 1,
            "filter[automation_state]": "workflows",
            "page": 2,
            "limit": 10,
            "sort": "-created_at",
            "with_steps": 1,
        },
        None,
    ),
    (
        "activity",
        [1],
        {
            "filter": {"status": "active", "search": "a@example.com"},
            "page": 1,
            "limit": 10,
            "sort": "-updated_at",
        },
        "GET",
        "/automations/1/activity",
        {
            "filter[status]": "active",
            "filter[search]": "a@example.com",
            "page": 1,
            "limit": 10,
            "sort": "-updated_at",
        },
        None,
    ),
    (
        "create",
        ["Welcome"],
        {},
        "POST",
        "/automations",
        None,
        {"name": "Welcome"},
    ),
    (
        "update",
        [1, "Welcome"],
        {"trigger_data": {"repeatable": True}, "triggers": []},
        "PUT",
        "/automations/1",
        None,
        {
            "name": "Welcome",
            "trigger_data": {"repeatable": True},
            "triggers": [],
        },
    ),
    ("copy", [1], {}, "POST", "/automations/1/copy", None, None),
    ("enable", [1], {}, "POST", "/automations/1/enable", None, None),
    ("disable", [1], {}, "POST", "/automations/1/disable", None, None),
    (
        "test",
        [1, "a@example.com"],
        {},
        "POST",
        "/automations/1/test",
        None,
        {"email": "a@example.com"},
    ),
    (
        "add_subscribers",
        [1],
        {"step_id": 2, "emails": ["a@example.com"], "groups": [3]},
        "POST",
        "/automations/1/add-subscribers",
        None,
        {"step_id": 2, "emails": ["a@example.com"], "groups": [3]},
    ),
    (
        "readd",
        [1, "selected_step", {"status": "completed"}],
        {"selected_step_id": "2"},
        "POST",
        "/automations/1/readd",
        None,
        {
            "readd_subscribers_to": "selected_step",
            "filter": {"status": "completed"},
            "selected_step_id": "2",
        },
    ),
    (
        "activity_add_to_group",
        [1, ["3"], {"status": "active"}],
        {},
        "POST",
        "/automations/1/activity/add-to-group",
        None,
        {"destination_groups": ["3"], "filter": {"status": "active"}},
    ),
    (
        "activity_cancel_automation",
        [1, {"status": "active", "id": ["5"]}],
        {},
        "POST",
        "/automations/1/activity/cancel-automation",
        None,
        {"filter": {"status": "active", "id": ["5"]}},
    ),
    (
        "activity_skip_delay",
        [1, {"status": "active"}],
        {},
        "POST",
        "/automations/1/activity/skip-delay",
        None,
        {"filter": {"status": "active"}},
    ),
    ("list_triggers", [1], {}, "GET", "/automations/1/triggers", None, None),
    (
        "create_trigger",
        [1, "subscriber_joins_group"],
        {"data": {"group_ids": [3]}},
        "POST",
        "/automations/1/triggers",
        None,
        {"type": "subscriber_joins_group", "data": {"group_ids": [3]}},
    ),
    ("get_trigger", [1, 4], {}, "GET", "/automations/1/triggers/4", None, None),
    (
        "update_trigger",
        [1, 4],
        {"data": {"group_ids": [3]}},
        "PUT",
        "/automations/1/triggers/4",
        None,
        {"data": {"group_ids": [3]}},
    ),
    ("list_steps", [1], {}, "GET", "/automations/1/steps/index", None, None),
    (
        "create_step",
        [1, "delay"],
        {
            "parent_id": 2,
            "branch": "yes",
            "move_to_branch": "no",
            "data": {"unit": "days", "value": 1},
        },
        "POST",
        "/automations/1/steps",
        None,
        {
            "type": "delay",
            "parent_id": 2,
            "branch": "yes",
            "move_to_branch": "no",
            "data": {"unit": "days", "value": 1},
        },
    ),
    ("get_step", [1, 2], {}, "GET", "/automations/1/steps/2", None, None),
    (
        "update_step",
        [1, 2],
        {
            "parent_id": 3,
            "data": {"unit": "days"},
            "reschedule_waiting_subscribers": True,
        },
        "PUT",
        "/automations/1/steps/2",
        None,
        {
            "parent_id": 3,
            "data": {"unit": "days"},
            "reschedule_waiting_subscribers": True,
        },
    ),
    (
        "copy_step",
        [1, 2],
        {"parent_id": 3, "branch": "yes", "move_to_branch": "no"},
        "POST",
        "/automations/1/steps/2/copy",
        None,
        {"parent_id": 3, "branch": "yes", "move_to_branch": "no"},
    ),
    (
        "reorder_steps",
        [1, 2],
        {"new_parent_step_id": 3, "branch": "yes", "branch_for_child": "no"},
        "POST",
        "/automations/1/steps/reorder",
        None,
        {
            "dragged_step_id": 2,
            "new_parent_step_id": 3,
            "branch": "yes",
            "branch_for_child": "no",
        },
    ),
    (
        "select_ab_test_winner",
        [1, 2, "a_path"],
        {},
        "PUT",
        "/automations/1/steps/2/select-ab-test-winner",
        None,
        {"ab_test_winner": "a_path"},
    ),
    (
        "get_email_content",
        [1, 6],
        {},
        "GET",
        "/automations/1/emails/6/content",
        None,
        None,
    ),
    (
        "update_email_content",
        [1, 6],
        {"html": "<p>Hi</p>"},
        "PUT",
        "/automations/1/emails/6/content",
        None,
        {"html": "<p>Hi</p>"},
    ),
    (
        "email_report_stats",
        [1, 6],
        {
            "start_date": "2026-01-01",
            "end_date": "2026-02-01",
            "shop_id": "7",
            "excel": False,
        },
        "GET",
        "/automations/1/emails/6/report-stats",
        {
            "start_date": "2026-01-01",
            "end_date": "2026-02-01",
            "shop_id": "7",
            "excel": 0,
        },
        None,
    ),
    (
        "email_unsubscribe_reasons",
        [1, 6],
        {},
        "GET",
        "/automations/1/emails/6/unsubscribe-reasons",
        None,
        None,
    ),
    (
        "list_templates",
        [],
        {"filter": {"type": "free", "category": 2}, "limit": 10, "page": 1},
        "GET",
        "/automation-templates",
        {"filter[type]": "free", "filter[category]": 2, "limit": 10, "page": 1},
        None,
    ),
    (
        "select_template",
        [8],
        {},
        "POST",
        "/automations/select-template/8",
        None,
        None,
    ),
    (
        "steps_run_counts",
        [1],
        {},
        "GET",
        "/automations/1/steps/run-counts",
        None,
        None,
    ),
    (
        "step_run_counts",
        [1, 2],
        {},
        "GET",
        "/automations/1/steps/run-counts/2",
        None,
        None,
    ),
    (
        "triggers_run_counts",
        [1],
        {},
        "GET",
        "/automations/1/triggers/run-counts",
        None,
        None,
    ),
    (
        "trigger_run_counts",
        [1, 4],
        {},
        "GET",
        "/automations/1/triggers/run-counts/4",
        None,
        None,
    ),
    (
        "ab_steps_stats",
        [1],
        {},
        "GET",
        "/automations/1/ab-steps-stats",
        None,
        None,
    ),
    (
        "ab_step_stats",
        [1, 2],
        {},
        "GET",
        "/automations/1/ab-steps-stats/2",
        None,
        None,
    ),
    (
        "step_subscribers",
        [1, 2, "queued"],
        {
            "filter": {"search": "a@example.com", "id": ["9", "10"]},
            "page": 1,
            "limit": 10,
            "sort": "-date",
        },
        "GET",
        "/automations/1/activity/steps/2/subscribers",
        {
            "status": "queued",
            "filter[search]": "a@example.com",
            "filter[id]": "9,10",
            "page": 1,
            "limit": 10,
            "sort": "-date",
        },
        None,
    ),
    (
        "trigger_subscribers",
        [1, 4, "completed"],
        {"filter": {"date_from": "2026-01-01", "date_to": "2026-02-01"}},
        "GET",
        "/automations/1/activity/triggers/4/subscribers",
        {
            "status": "completed",
            "filter[date_from]": "2026-01-01",
            "filter[date_to]": "2026-02-01",
        },
        None,
    ),
    (
        "email_monthly_totals",
        [1],
        {
            "start_date": "2026-01-01",
            "end_date": "2026-02-01",
            "shop_id": "7",
            "excel": True,
        },
        "GET",
        "/automations/1/monthly-totals/email",
        {
            "start_date": "2026-01-01",
            "end_date": "2026-02-01",
            "shop_id": "7",
            "excel": 1,
        },
        None,
    ),
]


DELETE_CASES = [
    ("delete", [1], "/automations/1"),
    ("delete_trigger", [1, 4], "/automations/1/triggers/4"),
    ("delete_step", [1, 2], "/automations/1/steps/2"),
]


UNKNOWN_ARGUMENT_CASES = [
    ("list", []),
    ("activity", [1]),
    ("update", [1, "Welcome"]),
    ("add_subscribers", [1]),
    ("create_step", [1, "delay"]),
    ("delete_step", [1, 2]),
    ("list_templates", []),
    ("step_subscribers", [1, 2, "queued"]),
]


NO_CONTENT_CASES = [
    ("test", [1, "a@example.com"], {}),
    ("add_subscribers", [1], {"emails": ["a@example.com"]}),
    ("readd", [1, "last_completed_step", {"status": "completed"}], {}),
    ("activity_add_to_group", [1, ["3"], {"status": "active"}], {}),
    ("activity_cancel_automation", [1, {"status": "active"}], {}),
    ("activity_skip_delay", [1, {"status": "active"}], {}),
]


class TestAutomationsRequests:
    @classmethod
    def setup_class(self):
        self.client = MailerLite.Client({"api_key": "test"})

    @pytest.mark.parametrize(
        "method_name, args, kwargs, verb, path, params, body",
        REQUEST_CASES,
        ids=_method_ids(REQUEST_CASES),
    )
    def test_method_sends_documented_request(
        self, sent_request, method_name, args, kwargs, verb, path, params, body
    ):
        getattr(self.client.automations, method_name)(*args, **kwargs)

        request = sent_request()
        assert request.method == verb
        assert request.path == path
        assert (request.params or None) == params
        assert request.body == body

    @pytest.mark.parametrize(
        "method_name, args, path",
        DELETE_CASES,
        ids=_method_ids(DELETE_CASES),
    )
    def test_delete_method_sends_documented_request_and_returns_true(
        self, sent_request, method_name, args, path
    ):
        response = getattr(self.client.automations, method_name)(*args)

        request = sent_request()
        assert response is True
        assert request.method == "DELETE"
        assert request.path == path

    def test_activity_sends_with_subscribers_only_when_truthy(self, sent_request):
        self.client.automations.activity(
            1, filter={"status": "active"}, with_subscribers=True
        )
        assert sent_request().params == {
            "filter[status]": "active",
            "with_subscribers": 1,
        }

        for value in (False, None):
            self.client.automations.activity(
                1, filter={"status": "active"}, with_subscribers=value
            )
            assert sent_request().params == {"filter[status]": "active"}

    def test_delete_step_sends_branch_to_delete(self, sent_request):
        self.client.automations.delete_step(1, 2, branch_to_delete="yes")

        assert sent_request().params == {"branch_to_delete": "yes"}

    @pytest.mark.parametrize(
        "method_name, args",
        UNKNOWN_ARGUMENT_CASES,
        ids=_method_ids(UNKNOWN_ARGUMENT_CASES),
    )
    def test_method_rejects_unknown_argument(self, sent_request, method_name, args):
        with pytest.raises(TypeError):
            getattr(self.client.automations, method_name)(*args, unknown=True)

    @pytest.mark.parametrize(
        "method_name, args, kwargs",
        NO_CONTENT_CASES,
        ids=_method_ids(NO_CONTENT_CASES),
    )
    def test_no_content_method_returns_true_without_reading_body(
        self, mocker, method_name, args, kwargs
    ):
        response = mocker.Mock(status_code=204)
        response.json.side_effect = ValueError("no body")
        mocker.patch("mailerlite.api_client.requests.request", return_value=response)

        result = getattr(self.client.automations, method_name)(*args, **kwargs)

        assert result is True
        response.json.assert_not_called()
