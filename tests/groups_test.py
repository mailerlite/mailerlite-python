import os
import random
import string

import mailerlite as MailerLite
import pytest
import vcr
from dotenv import load_dotenv
from pytest import fixture


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


class TestGroups:
    @classmethod
    def setup_class(self):
        load_dotenv()

        self.client = MailerLite.Client({"api_key": os.getenv("API_KEY")})

    def test_api_url_is_properly_set(self):
        assert self.client.groups.base_api_url == "api/groups"

    def test_given_incorrect_name_when_calling_create_then_group_create_will_fail(self):
        name = "".join(random.choices(string.ascii_letters, k=300))

        with pytest.raises(ValueError):
            self.client.groups.create(name)

    @vcr.use_cassette(
        "tests/vcr_cassettes/groups-create.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_parameters_when_calling_create_then_group_is_created(
        self, group_keys
    ):
        name = "Test group"
        response = self.client.groups.create(name)

        pytest.entity_id = int(response["data"]["id"])

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(group_keys).issubset(response["data"].keys())
        assert response["data"]["name"] == name

    @vcr.use_cassette(
        "tests/vcr_cassettes/groups-list.yml", filter_headers=["Authorization"]
    )
    def test_list_of_all_groups_should_be_returned(self, group_keys):
        response = self.client.groups.list(limit=10, page=1)

        assert isinstance(response, dict)
        assert isinstance(response["data"][0], dict)
        assert set(group_keys).issubset(response["data"][0].keys())

    def test_given_incorrect_group_id_when_calling_update_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.groups.update("1234", "name")

    @vcr.use_cassette(
        "tests/vcr_cassettes/groups-update.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_group_id_and_name_when_calling_update_then_group_is_updated(
        self, group_keys
    ):
        """Tests an API call for updating existing subscriber group"""

        name = "New group name"
        response = self.client.groups.update(pytest.entity_id, name)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(group_keys).issubset(response["data"].keys())
        assert response["data"]["name"] == name

    def test_given_incorrect_group_id_when_calling_get_group_subscribers_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.groups.get_group_subscribers("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/groups-get-subscribers-in-group.yml",
        filter_headers=["Authorization"],
    )
    def test_given_correct_group_id_when_calling_get_group_subscribers_then_list_of_subscribers_is_returned(
        self, subscriber_keys
    ):
        # This test requires at least one subscriber assigned to a group
        response = self.client.groups.get_group_subscribers(
            pytest.entity_id, limit=5, cursor=1
        )

        assert isinstance(response, dict)
        assert isinstance(response["data"], list)

        if len(response["data"]) > 0:
            assert isinstance(response["data"][0], dict)
            assert set(subscriber_keys).issubset(response["data"][0].keys())

    def test_given_incorrect_group_id_when_calling_delete_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.groups.delete("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/groups-delete.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_group_id_when_calling_delete_then_group_is_removed(
        self, group_keys
    ):
        """Tests an API call for deleting existing subscriber group"""

        response = self.client.groups.delete(pytest.entity_id)

        assert response is True

        id = 121212
        response = self.client.groups.delete(id)

        assert response is False
