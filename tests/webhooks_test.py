import os

import mailerlite as MailerLite
import pytest
import requests
import vcr
from dotenv import load_dotenv
from pytest import fixture


@fixture
def webhook_keys():
    return [
        "id",
        "name",
        "url",
        "events",
        "enabled",
        "secret",
        "created_at",
        "updated_at",
    ]


class TestWebhooks:
    @classmethod
    def setup_class(self):
        load_dotenv()

        self.client = MailerLite.Client({"api_key": os.getenv("API_KEY")})

    def test_api_url_is_properly_set(self):
        assert self.client.webhooks.base_api_url == "api/webhooks"

    def test_given_incorrect_parameters_when_calling_create_then_creating_a_webhook_will_fail(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.webhooks.create({}, "http", "Test")

    @vcr.use_cassette(
        "tests/vcr_cassettes/webhooks-create.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_params_when_calling_create_then_webhook_is_created(
        self, webhook_keys
    ):
        name = "My Webhooks"
        events = ["subscriber.created", "subscriber.unsubscribed"]
        url = "https://mailerlite.com"
        response = self.client.webhooks.create(events, url, name)

        pytest.entity_id = int(response["data"]["id"])

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(webhook_keys).issubset(response["data"].keys())

    @vcr.use_cassette(
        "tests/vcr_cassettes/webhooks-list.yml", filter_headers=["Authorization"]
    )
    def test_list_of_all_webhooks_should_be_returned(self, webhook_keys):
        response = self.client.webhooks.list()

        assert isinstance(response, dict)
        assert isinstance(response["data"], list)
        assert isinstance(response["data"][0], dict)
        assert set(webhook_keys).issubset(response["data"][0].keys())

    def test_given_incorrect_webhook_id_when_calling_get_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.webhooks.get("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/webhooks-get.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_webhook_id_when_calling_get_then_webhook_is_returned(
        self, webhook_keys
    ):
        response = self.client.webhooks.get(pytest.entity_id)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(webhook_keys).issubset(response["data"].keys())

    def test_given_incorrect_webhook_id_when_calling_update_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.webhooks.update("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/webhooks-update.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_webhook_id_and_params_when_calling_update_then_webhook_is_updated(
        self, webhook_keys
    ):
        name = "My New Webhook Name"
        response = self.client.webhooks.update(pytest.entity_id, name=name)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(webhook_keys).issubset(response["data"].keys())

    def test_given_incorrect_webhook_id_when_calling_delete_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.webhooks.delete("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/webhooks-delete.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_webhook_id_when_calling_delete_then_webhook_is_removed(self):
        """Tests an API call for webhook the field"""

        response = self.client.webhooks.delete(int(pytest.entity_id))
        assert response is True

        with pytest.raises(requests.HTTPError):
            self.client.webhooks.delete(121212)
