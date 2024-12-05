import os

import mailerlite as MailerLite
import pytest
import vcr
from dotenv import load_dotenv
from pytest import fixture


@fixture
def form_keys():
    return [
        "id",
        "type",
        "slug",
        "name",
        "created_at",
        "conversions_count",
        "opens_count",
        "conversion_rate",
        "settings",
        "last_registration_at",
        "active",
        "is_broken",
        "has_content",
        "can",
        "used_in_automations",
        "warnings",
        "double_optin",
        "screenshot_url",
    ]


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


class TestForms:
    @classmethod
    def setup_class(self):
        load_dotenv()

        self.client = MailerLite.Client({"api_key": os.getenv("API_KEY")})

    def test_api_url_is_properly_set(self):
        assert self.client.forms.base_api_url == "api/forms"

    @vcr.use_cassette(
        "tests/vcr_cassettes/forms-list.yml", filter_headers=["Authorization"]
    )
    def test_list_of_all_forms_should_be_returned(self, form_keys):
        # This test requires previously created form

        type = "popup"
        response = self.client.forms.list(type, limit=10, page=1, sort="name")

        pytest.entity_id = int(response["data"][0]["id"])

        assert isinstance(response, dict)
        assert isinstance(response["data"], list)
        assert isinstance(response["data"][0], dict)
        assert set(form_keys).issubset(response["data"][0].keys())

    def test_given_incorrect_form_id_when_calling_get_then_type_error_is_returned(self):
        with pytest.raises(TypeError):
            self.client.forms.get("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/forms-get.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_form_id_when_calling_get_then_form_is_returned(
        self, form_keys
    ):
        """Tests an API call for getting information about one form"""

        response = self.client.forms.get(pytest.entity_id)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(form_keys).issubset(response["data"].keys())

    def test_given_incorrect_form_id_when_calling_update_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.forms.update("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/forms-update.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_form_id_and_name_when_calling_update_then_form_is_updated(
        self, form_keys
    ):
        name = "New Form Name"
        response = self.client.forms.update(pytest.entity_id, name)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(form_keys).issubset(response["data"].keys())
        assert response["data"]["name"] == name

    def test_given_incorrect_form_id_when_calling_get_subscribers_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.forms.get_subscribers("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/forms-get-subscribers.yml",
        filter_headers=["Authorization"],
    )
    def test_given_correct_form_id_when_calling_get_subscribers_then_list_of_signed_up_subscribers_is_returned(
        self, subscriber_keys
    ):
        # This test requires manually generated activity on a form
        response = self.client.forms.get_subscribers(
            pytest.entity_id, page=1, limit=20, filter={"status": "active"}
        )

        assert isinstance(response, dict)
        assert isinstance(response["data"], list)

        # Prevent test to fail if there is no subscriber activity
        if len(response["data"]) > 0:
            assert set(subscriber_keys).issubset(response["data"][0].keys())

    def test_given_incorrect_form_id_when_calling_delete_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.forms.delete("1234")

    # @vcr.use_cassette(
    #     "tests/vcr_cassettes/forms-delete.yml", filter_headers=["Authorization"]
    # )
    # def test_given_correct_form_id_when_calling_delete_then_form_is_removed(self):
    #     """Tests an API call for deleting a form"""

    #     response = self.client.forms.delete(pytest.entity_id)
    #     assert response is True

    #     response = self.client.forms.delete(111)
    #     assert response is False
