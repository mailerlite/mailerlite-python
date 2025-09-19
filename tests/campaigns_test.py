import os
from datetime import datetime, timedelta

import mailerlite as MailerLite
import pytest
import vcr
from dotenv import load_dotenv
from pytest import fixture


@fixture
def campaign_keys():
    return [
        "id",
        "account_id",
        "name",
        "type",
        "status",
        "settings",
        "filter",
        "filter_for_humans",
        "delivery_schedule",
        "language_id",
        "updated_at",
        "scheduled_for",
        "queued_at",
        "started_at",
        "finished_at",
        "stopped_at",
        "default_email_id",
        "emails",
        "used_in_automations",
        "type_for_humans",
        "is_stopped",
        "has_winner",
        "winner_version_for_human",
        "winner_sending_time_for_humans",
        "winner_selected_manually_at",
        "uses_ecommerce",
        "uses_survey",
        "can_be_scheduled",
        "warnings",
        "is_currently_sending_out",
    ]


@fixture
def campaign_activity_keys():
    return ["id", "opens_count", "clicks_count"]


@fixture
def campaign_language_keys():
    return ["id", "shortcode", "iso639", "name", "direction"]


class TestCampaigns:
    @classmethod
    def setup_class(self):
        load_dotenv()

        self.client = MailerLite.Client({"api_key": os.getenv("API_KEY")})

    def test_api_url_is_properly_set(self):
        assert self.client.campaigns.base_api_url == "api/campaigns"

    @vcr.use_cassette(
        "tests/vcr_cassettes/campaign-create.yml", filter_headers=["Authorization"]
    )
    def test_given_proper_parameters_when_user_calls_create_then_new_campaign_is_created(
        self, campaign_keys
    ):
        params = {
            "name": "Test Campaign",
            "language_id": 1,
            "type": "regular",
            "emails": [
                {
                    "subject": "This is a test campaign",
                    "from_name": "Test Man",
                    "from": "sdk@igor.fail",
                    "content": "<html><body><h1>Test</h1></body></html>",
                }
            ],
        }

        response = self.client.campaigns.create(params)
        pytest.entity_id = response["data"]["id"]

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(campaign_keys).issubset(response["data"].keys())
        assert response["data"]["name"] == params["name"]
        assert int(response["data"]["language"]["id"]) == params["language_id"]
        assert response["data"]["type"] == params["type"]

    def test_given_incorrect_campaign_id_when_calling_update_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.campaigns.update("1234", {})

    @vcr.use_cassette(
        "tests/vcr_cassettes/campaign-update.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_parameters_when_user_calls_update_then_existing_campaign_is_updated(
        self, campaign_keys
    ):
        params = {
            "name": "New Campaign Name",
            "language_id": 1,
            "emails": [
                {
                    "subject": "This is a new test campaign subject",
                    "from_name": "Test Man",
                    "from": "sdk@igor.fail",
                }
            ],
        }

        response = self.client.campaigns.update(int(pytest.entity_id), params)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(campaign_keys).issubset(response["data"].keys())
        assert response["data"]["name"] == params["name"]
        assert int(response["data"]["language_id"]) == params["language_id"]

    def test_given_incorrect_campaign_id_when_calling_get_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.campaigns.get("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/campaign-get.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_campaign_id_when_calling_get_then_campaign_is_returned(
        self, campaign_keys
    ):
        response = self.client.campaigns.get(int(pytest.entity_id))

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        assert set(campaign_keys).issubset(response["data"].keys())

    @vcr.use_cassette(
        "tests/vcr_cassettes/campaign-list.yml", filter_headers=["Authorization"]
    )
    def test_list_of_all_campaigns_should_be_returned(self, campaign_keys):
        response = self.client.campaigns.list(
            limit=10, page=1, filter={"status": "draft"}
        )

        assert isinstance(response, dict)
        assert isinstance(response["data"], list)
        assert isinstance(response["data"][0], dict)
        assert set(campaign_keys).issubset(response["data"][0].keys())

    def test_given_incorrect_campaign_id_when_calling_schedule_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.campaigns.schedule("1234", {})

    @vcr.use_cassette(
        "tests/vcr_cassettes/campaign-schedule.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_campaign_id_and_schedule_parameters_when_calling_schedule_then_campaign_schedule_is_updated(
        self,
    ):
        date = datetime.now() + timedelta(days=2)
        date = date.strftime("%Y-%m-%d")

        params = {
            "delivery": "scheduled",
            "schedule": {"date": date, "hours": "22", "minutes": "00"},
        }

        response = self.client.campaigns.schedule(int(pytest.entity_id), params)

        assert isinstance(response, dict)
        assert isinstance(response["data"], dict)
        schedule_date = datetime.strptime(
            response["data"]["scheduled_for"], "%Y-%m-%d %H:%M:%S"
        )
        assert schedule_date.date().strftime("%Y-%m-%d") == date

    def test_given_incorrect_campaign_id_when_calling_cancel_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.campaigns.cancel("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/campaign-cancel.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_campaign_id_when_calling_cancel_then_campaign_is_going_to_be_cancelled(
        self,
    ):
        response = self.client.campaigns.cancel(int(pytest.entity_id))

        assert response["data"]["status"] == "draft"

    def test_given_incorrect_campaign_id_when_calling_delete_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.campaigns.delete("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/campaign-delete.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_campaign_id_when_calling_delete_then_campaign_is_removed(
        self,
    ):
        response = self.client.campaigns.delete(int(pytest.entity_id))

        assert response is True

        response = self.client.campaigns.delete(121212)

        assert response is False

    def test_given_incorrect_campaign_id_when_calling_activity_then_type_error_is_returned(
        self,
    ):
        with pytest.raises(TypeError):
            self.client.campaigns.activity("1234")

    @vcr.use_cassette(
        "tests/vcr_cassettes/campaign-activity.yml", filter_headers=["Authorization"]
    )
    def test_given_correct_campaign_id_when_calling_activity_then_campaign_activity_information_is_returned(
        self, campaign_activity_keys
    ):
        response = self.client.campaigns.activity(139788917762163910)

        print(response["data"][0].keys())
        assert isinstance(response, dict)
        assert isinstance(response["data"], list)
        assert set(campaign_activity_keys).issubset(response["data"][0].keys())

    @vcr.use_cassette(
        "tests/vcr_cassettes/campaign-languages.yml", filter_headers=["Authorization"]
    )
    def test_list_of_all_supported_languages_in_campaign(self, campaign_language_keys):
        response = self.client.campaigns.languages()

        assert isinstance(response, dict)
        assert isinstance(response["data"], list)
        assert set(campaign_language_keys).issubset(response["data"][0].keys())
