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
def segment_keys():
    return ["id", "name", "total", "open_rate", "click_rate", "created_at"]


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


class TestSegments:
    """
    Before running these tests make sure that at least one segment exist
    """

    @classmethod
    def setup_class(self):
        load_dotenv()

        self.client = MailerLite.Client({"api_key": os.getenv("API_KEY")})

    def test_api_url_is_properly_set(self):
        assert self.client.segments.base_api_url == "api/segments"

    @vcr.use_cassette(
        "tests/vcr_cassettes/segments-list.yml", filter_headers=["Authorization"]
    )
    def test_list_of_all_segments_should_be_returned(self, segment_keys):
        response = self.client.segments.list(limit=10, page=1)

        # Set segment_id for future tests
        if len(response["data"]) > 0:
            pytest.entity_id = int(response["data"][0]["id"])

        assert isinstance(response, dict)
        assert isinstance(response["data"][0], dict)
        assert set(segment_keys).issubset(response["data"][0].keys())

    def test_given_incorrect_segment_id_when_calling_get_subscribers_list_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.segments.get_subscribers("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/segments-get.yml",
        filter_headers=["Authorization"],
    )
    def test_given_valid_segment_id_when_calling_get_segment_is_returned(
        self, segment_keys
    ):
        if pytest.entity_id and pytest.entity_id == 0:
            pytest.skip("segment_id is not set")

        response = self.client.segments.get(pytest.entity_id)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(segment_keys).issubset(response["data"].keys())

    @vcr.use_cassette(
        "tests/vcr_cassettes/segments-get-subscribers.yml",
        filter_headers=["Authorization"],
    )
    def test_given_valid_segment_id_when_calling_get_subscribers_list_of_subscribers_in_segment_is_returned(
        self, subscriber_keys
    ):
        if pytest.entity_id and pytest.entity_id == 0:
            pytest.skip("segment_id is not set")

        response = self.client.segments.get_subscribers(pytest.entity_id)

        assert isinstance(response, dict)
        assert set(subscriber_keys).issubset(response["data"][0].keys())

    def test_given_incorrect_segment_id_when_calling_update_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.segments.update("1234", "name")

    def test_given_invalid_name_when_calling_update_then_segment_update_will_fail(self):
        name = "".join(random.choices(string.ascii_letters, k=300))
        segment_id = 123

        with pytest.raises(ValueError):
            self.client.segments.update(segment_id, name)

    @vcr.use_cassette(
        "tests/vcr_cassettes/segments-update.yml", filter_headers=["Authorization"]
    )
    def test_given_valid_name_and_segment_id_when_calling_update_then_segment_is_updated(
        self,
    ):
        if pytest.entity_id and pytest.entity_id == 0:
            pytest.skip("segment_id is not set")

        name = "New Name"
        response = self.client.segments.update(pytest.entity_id, name)

        assert response is True

        with pytest.raises(requests.HTTPError):
            self.client.segments.update(123123, name)

    def test_given_incorrect_segment_id_when_calling_delete_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.segments.delete("1234")

    # @vcr.use_cassette(
    #     "tests/vcr_cassettes/segments-delete.yml", filter_headers=["Authorization"]
    # )
    # def test_given_valid_segment_id_when_calling_id_then_segment_is_removed(
    #     self, segment_keys
    # ):
    #     if pytest.entity_id and pytest.entity_id == 0:
    #         pytest.skip("segment_id is not set")

    #     response = self.client.segments.delete(pytest.entity_id)

    #     assert response is True

    #     segment_id = 123123
    #     response = self.client.segments.delete(segment_id)

    #     assert response is False


class TestSegmentsRequests:
    @classmethod
    def setup_class(self):
        self.client = MailerLite.Client({"api_key": "test"})

    def test_list_sends_documented_query_params(self, sent_request):
        self.client.segments.list(limit=10, page=2, sort="name")

        request = sent_request()
        assert request.method == "GET"
        assert request.path == "/segments"
        assert request.params == {"limit": 10, "page": 2, "sort": "name"}

    def test_get_subscribers_sends_cursor_and_filter_status(self, sent_request):
        self.client.segments.get_subscribers(
            123, filter={"status": "active"}, limit=10, cursor="abc"
        )

        request = sent_request()
        assert request.method == "GET"
        assert request.path == "/segments/123/subscribers"
        assert request.params == {
            "filter[status]": "active",
            "limit": 10,
            "cursor": "abc",
        }

    def test_get_subscribers_still_sends_after(self, sent_request):
        self.client.segments.get_subscribers(123, after="abc")

        assert sent_request().params == {"after": "abc"}

    def test_get_subscribers_sends_after_and_cursor_together(self, sent_request):
        self.client.segments.get_subscribers(123, after="old", cursor="new")

        assert sent_request().params == {"after": "old", "cursor": "new"}

    def test_update_sends_documented_body_params(self, sent_request):
        rules = [[{"operator": "in_any", "args": ["groups", 1]}]]
        response = self.client.segments.update(123, "New name", filter=rules)

        request = sent_request()
        assert response is True
        assert request.method == "PUT"
        assert request.path == "/segments/123"
        assert request.body == {"name": "New name", "filter": rules}

    def test_update_rejects_unknown_argument(self, sent_request):
        with pytest.raises(TypeError):
            self.client.segments.update(123, "New name", unknown=True)
