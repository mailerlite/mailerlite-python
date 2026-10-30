import os
import random
import string

import pytest
import requests
import vcr
from dotenv import load_dotenv
from pytest import fixture

import mailerlite as MailerLite


@fixture
def subscriber_keys():
    return [
        "id",
        "email",
        "status",
        "source",
        "sent",
        "opens_count",
        "click_rate",
        "ip_address",
        "subscribed_at",
        "unsubscribed_at",
        "created_at",
        "updated_at",
    ]


@fixture
def import_keys():
    return [
        "id",
        "total",
        "processed",
        "imported",
        "updated",
        "errored",
        "percent",
        "done",
        "invalid",
        "invalid_count",
        "mistyped",
        "mistyped_count",
        "changed",
        "changed_count",
        "unchanged",
        "unchanged_count",
        "unsubscribed",
        "unsubscribed_count",
        "role_based",
        "role_based_count",
        "banned_import_emails_count",
        "updated_at",
        "undone_at",
        "stopped_at",
        "undo_started_at",
        "finished_at",
    ]


@fixture
def group_keys():
    return [
        "id",
        "name",
        "active_count",
        "sent_count",
        "opens_count",
        "open_rate",
        "clicks_count",
        "click_rate",
        "unsubscribed_count",
        "unconfirmed_count",
        "bounced_count",
        "junk_count",
    ]


class TestSubscribers:
    # Set static import_id
    import_id = 139791107607233967

    @classmethod
    def setup_class(self):
        load_dotenv()

        self.client = MailerLite.Client({"api_key": os.getenv("API_KEY")})

    def test_api_url_is_properly_set(self):
        assert self.client.subscribers.base_api_url == "api/subscribers"

    @vcr.use_cassette(
        "tests/vcr_cassettes/subscribers-list.yml", filter_headers=["Authorization"]
    )
    def test_list_of_all_subscribers_should_be_returned(self, subscriber_keys):
        response = self.client.subscribers.list(limit=10)

        assert isinstance(response, dict)
        assert isinstance(response["data"], list)
        assert isinstance(response["data"][0], dict)
        assert set(subscriber_keys).issubset(response["data"][0].keys())

    def test_given_invalid_email_address_when_calling_create_then_create_subscriber_will_fail(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.subscribers.create("wrong2mail.com")

    def test_given_invalid_param_when_caling_create_then_create_subscriber_will_fail(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.subscribers.create("some@email.com", unknownparam=1)

    def test_given_invalid_fields_or_groups_params_when_calling_create_then_create_subscriber_will_fail(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.subscribers.create("some@email.com", fields=[])

        with pytest.raises(TypeError):
            self.client.subscribers.create("some@email.com", groups={})

    @vcr.use_cassette(
        "tests/vcr_cassettes/subscribers-create.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_params_when_calling_create_then_subscirber_is_created(
        self, subscriber_keys
    ):
        response = self.client.subscribers.create(
            "test5@email.com",
            fields={"name": "John", "last_name": "Doe"},
            ip_address="1.1.1.1",
        )

        pytest.entity_id = int(response["data"]["id"])
        pytest.entity_email = response["data"]["email"]

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(subscriber_keys).issubset(response["data"].keys())

    @vcr.use_cassette(
        "tests/vcr_cassettes/subscribers-update.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_params_when_calling_update_then_subscirber_is_updated(
        self, subscriber_keys
    ):
        response = self.client.subscribers.update(
            pytest.entity_email,
            fields={"name": "Someone", "last_name": "Doe"},
            ip_address="1.1.1.1",
        )

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(subscriber_keys).issubset(response["data"].keys())
        assert response["data"]["fields"]["last_name"] == "Doe"

    def test_given_invalid_subscriber_id_when_calling_get_then_returning_subscirber_will_fail(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.subscribers.get("abcdefgh")

    @vcr.use_cassette(
        "tests/vcr_cassettes/subscribers-get-email.yml",
        filter_headers=["Authorization"],
    )
    def test_given_subscriber_email_calling_get_then_subscirber_is_returned(
        self, subscriber_keys
    ):
        response = self.client.subscribers.get(pytest.entity_email)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(subscriber_keys).issubset(response["data"].keys())

    @vcr.use_cassette(
        "tests/vcr_cassettes/subscribers-get-id.yml", filter_headers=["Authorization"]
    )
    def test_given_subscriber_id_calling_get_then_subscirber_is_returned(
        self, subscriber_keys
    ):
        response = self.client.subscribers.get(pytest.entity_id)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(subscriber_keys).issubset(response["data"].keys())

    @vcr.use_cassette(
        "tests/vcr_cassettes/subscribers-get-import.yml",
        filter_headers=["Authorization"],
    )
    def test_given_correct_import_id_when_calling_get_import_then_import_information_is_returned(
        self, import_keys
    ):
        response = self.client.subscribers.get_import(self.import_id)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(import_keys).issubset(response["data"].keys())

    @vcr.use_cassette(
        "tests/vcr_cassettes/subscribers-assign-subscriber-to-group.yml",
        record_mode="new_episodes",
        filter_headers=["Authorization"],
    )
    def test_given_correct_subscriber_id_and_grop_id_when_calling_assign_subscriber_to_group_then_subscriber_is_assigned(
        self, group_keys
    ):
        subscriber = self.client.subscribers.create(
            "grouptest@email.com",
            fields={"name": "John", "last_name": "Doe"},
            ip_address="1.1.1.1",
        )
        name = "".join(random.choices(string.ascii_letters, k=10))
        group = self.client.groups.create(name)
        response = self.client.subscribers.assign_subscriber_to_group(
            int(subscriber["data"]["id"]), int(group["data"]["id"])
        )

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(group_keys).issubset(response["data"].keys())

        self.client.subscribers.delete(int(subscriber["data"]["id"]))
        self.client.groups.delete(int(group["data"]["id"]))

    @vcr.use_cassette(
        "tests/vcr_cassettes/subscribers-unassign-subscriber-from-group.yml",
        record_mode="new_episodes",
        filter_headers=["Authorization"],
    )
    def test_given_correct_subscriber_id_and_grop_id_when_calling_unassign_subscriber_from_group_then_subscriber_is_unassigned(
        self,
    ):
        name = "".join(random.choices(string.ascii_letters, k=10))

        subscriber = self.client.subscribers.create(
            f"{name}@email.com",
            fields={"name": "John", "last_name": "Doe"},
            ip_address="1.1.1.1",
        )
        group = self.client.groups.create(name)
        self.client.subscribers.assign_subscriber_to_group(
            int(subscriber["data"]["id"]), int(group["data"]["id"])
        )
        response = self.client.subscribers.unassign_subscriber_from_group(
            int(subscriber["data"]["id"]), int(group["data"]["id"])
        )
        self.client.subscribers.delete(int(subscriber["data"]["id"]))
        self.client.groups.delete(int(group["data"]["id"]))

        assert response is True

    def test_given_invalid_subscriber_id_when_calling_delete_then_returning_subscirber_will_fail(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.subscribers.delete("abcdefgh")

    @vcr.use_cassette(
        "tests/vcr_cassettes/subscribers-delete.yml", filter_headers=["Authorization"]
    )
    def test_given_valid_subscriber_id_when_calling_delete_then_subscriber_is_deleted(
        self,
    ):
        response = self.client.subscribers.delete(pytest.entity_id)
        assert response is True

        with pytest.raises(requests.HTTPError):
            self.client.subscribers.delete(123123)

    @vcr.use_cassette(
        "tests/vcr_cassettes/subscribers-count.yml", filter_headers=["Authorization"]
    )
    def test_count_of_all_subscribers_should_be_returned(self, subscriber_keys):
        response = self.client.subscribers.count()

        assert isinstance(response, dict)
        assert "total" in response

    @vcr.use_cassette(
        "tests/vcr_cassettes/subscribers-forget.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_params_when_calling_forget_then_subscirber_is_marked_as_forgotten(
        self,
    ):
        user = self.client.subscribers.create(
            "test5@email.com",
            fields={"name": "John", "last_name": "Doe"},
            ip_address="1.1.1.1",
        )

        response = self.client.subscribers.forget(int(user["data"]["id"]))

        assert response is True


class TestSubscribersRequests:
    @classmethod
    def setup_class(self):
        self.client = MailerLite.Client({"api_key": "test"})

    def test_list_sends_documented_query_params(self, sent_request):
        self.client.subscribers.list(
            filter={"status": "active", "group": 1},
            limit=10,
            page=2,
            cursor="abc",
            sort="-created_at",
            include="groups",
            start_date="2026-01-01",
            end_date="2026-02-01",
            with_fields=True,
            with_groups=False,
        )

        request = sent_request()
        assert request.method == "GET"
        assert request.path == "/subscribers"
        assert request.params == {
            "filter[status]": "active",
            "filter[group]": 1,
            "limit": 10,
            "page": 2,
            "cursor": "abc",
            "sort": "-created_at",
            "include": "groups",
            "start_date": "2026-01-01",
            "end_date": "2026-02-01",
            "with_fields": 1,
            "with_groups": 0,
        }

    def test_create_sends_documented_body_params(self, sent_request):
        self.client.subscribers.create(
            "test@example.com",
            resubscribe=True,
            double_optin=True,
            notes="note",
            status="active",
        )

        request = sent_request()
        assert request.method == "POST"
        assert request.path == "/subscribers"
        assert request.body == {
            "email": "test@example.com",
            "resubscribe": True,
            "double_optin": True,
            "notes": "note",
            "status": "active",
        }

    def test_update_sends_put_to_subscriber_by_email(self, sent_request):
        self.client.subscribers.update(
            "test@example.com", fields={"name": "Someone"}, status="active"
        )

        request = sent_request()
        assert request.method == "PUT"
        assert request.path == "/subscribers/test@example.com"
        assert request.body == {"fields": {"name": "Someone"}, "status": "active"}

    def test_update_sends_put_to_subscriber_by_id(self, sent_request):
        self.client.subscribers.update(123, ip_address="1.1.1.1")

        request = sent_request()
        assert request.method == "PUT"
        assert request.path == "/subscribers/123"
        assert request.body == {"ip_address": "1.1.1.1"}

    def test_update_quotes_the_email_in_the_path(self, sent_request):
        self.client.subscribers.update("a+b#c@example.com", status="active")

        request = sent_request()
        assert request.method == "PUT"
        assert request.path == "/subscribers/a%2Bb%23c@example.com"
        assert request.body == {"status": "active"}

    def test_update_sends_new_email_as_email(self, sent_request):
        self.client.subscribers.update(123, new_email="new@example.com")

        request = sent_request()
        assert request.method == "PUT"
        assert request.path == "/subscribers/123"
        assert request.body == {"email": "new@example.com"}

    def test_activity_log_sends_documented_query_params(self, sent_request):
        self.client.subscribers.activity_log(
            123, filter={"log_name": "email_open"}, limit=5, page=1
        )

        request = sent_request()
        assert request.method == "GET"
        assert request.path == "/subscribers/123/activity-log"
        assert request.params == {
            "filter[log_name]": "email_open",
            "limit": 5,
            "page": 1,
        }

    def test_activity_log_rejects_unknown_argument(self, sent_request):
        with pytest.raises(TypeError):
            self.client.subscribers.activity_log(123, cursor="abc")
