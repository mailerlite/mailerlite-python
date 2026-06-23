import os
import random
import string

import mailerlite as MailerLite
import pytest
import requests
import vcr
from dotenv import load_dotenv
from pytest import fixture


@fixture
def field_keys():
    return ["id", "name", "key", "type"]


class TestFields:
    @classmethod
    def setup_class(self):
        load_dotenv()

        self.client = MailerLite.Client({"api_key": os.getenv("API_KEY")})

    def test_api_url_is_properly_set(self):
        assert self.client.fields.base_api_url == "api/fields"

    def test_given_incorrect_name_when_calling_create_then_creating_field_will_fail(
        self,
    ):
        name = "".join(random.choices(string.ascii_letters, k=300))
        type = "text"

        with pytest.raises(ValueError):
            self.client.fields.create(name, type)

        type = "unknown"
        with pytest.raises(ValueError):
            self.client.fields.create(name, type)

    @vcr.use_cassette(
        "tests/vcr_cassettes/fields-create.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_parameters_when_calling_create_then_field_is_created(
        self, field_keys
    ):
        name = "My Field"
        type = "text"
        response = self.client.fields.create(name, type)

        pytest.entity_id = int(response["data"]["id"])

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(field_keys).issubset(response["data"].keys())

    @vcr.use_cassette(
        "tests/vcr_cassettes/fields-list.yml", filter_headers=["Authorization"]
    )
    def test_list_of_all_fields_should_be_returned(self, field_keys):
        """Tests an API call for getting information about all fields"""

        response = self.client.fields.list(limit=10, page=1, sort="name")

        assert isinstance(response, dict)
        assert isinstance(response["data"], list)
        assert isinstance(response["data"][0], dict)
        assert set(field_keys).issubset(response["data"][0].keys())

    def test_given_incorrect_field_id_when_calling_update_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.fields.update("1234", "some name")

    @vcr.use_cassette(
        "tests/vcr_cassettes/fields-update.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_field_id_and_name_when_caling_update_then_field_is_updated(
        self, field_keys
    ):
        """Tests an API call for updating the field"""

        name = "My New Field Name"
        response = self.client.fields.update(field_id=pytest.entity_id, name=name)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(field_keys).issubset(response["data"].keys())

    def test_given_incorrect_field_id_when_calling_delete_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.fields.update("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/fields-delete.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_field_id_when_calling_delete_then_field_is_removed(
        self, field_keys
    ):
        """Tests an API call for deleting the field"""

        response = self.client.fields.delete(pytest.entity_id)
        assert response is True

        with pytest.raises(requests.HTTPError):
            self.client.fields.delete(121212)
