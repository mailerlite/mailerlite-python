import pytest

import mailerlite
from mailerlite.api_client import ApiClient
from mailerlite.response import ApiResponse


class TestApiResponse:
    def test_it_is_a_dict_with_the_decoded_body(self, mock_api):
        """Tests that ApiResponse has the decoded JSON body and the status code"""

        mock_api.add_response(201, {"data": {"id": "1"}}, {"X-Request-Id": "abc"})

        response = ApiResponse(ApiClient({}).request("POST", "api/emails/1/versions"))

        assert isinstance(response, dict)
        assert response == {"data": {"id": "1"}}
        assert response["data"]["id"] == "1"
        assert response.status_code == 201
        assert response.headers["x-request-id"] == "abc"

    def test_replayed_response_is_an_idempotent_replay(self, mock_api):
        """Tests that the Idempotent-Replayed header sets the replay flag"""

        mock_api.add_response(201, {"data": {}}, {"Idempotent-Replayed": "true"})

        response = ApiResponse(ApiClient({}).request("POST", "api/emails/1/blocks"))

        assert response.is_idempotent_replay is True

    @pytest.mark.parametrize("value", ["True", "TRUE", " true "])
    def test_replay_header_value_is_not_case_sensitive(self, mock_api, value):
        """Tests that a proxy can change the case of the Idempotent-Replayed value"""

        mock_api.add_response(201, {"data": {}}, {"Idempotent-Replayed": value})

        response = ApiResponse(ApiClient({}).request("POST", "api/emails/1/blocks"))

        assert response.is_idempotent_replay is True

    @pytest.mark.parametrize("value", ["false", "1", ""])
    def test_other_replay_header_values_are_not_an_idempotent_replay(
        self, mock_api, value
    ):
        """Tests that only the value true sets the replay flag"""

        mock_api.add_response(201, {"data": {}}, {"Idempotent-Replayed": value})

        response = ApiResponse(ApiClient({}).request("POST", "api/emails/1/blocks"))

        assert response.is_idempotent_replay is False

    def test_response_without_the_header_is_not_an_idempotent_replay(self, mock_api):
        """Tests that the replay flag is false without the Idempotent-Replayed header"""

        mock_api.add_response(201, {"data": {}})

        response = ApiResponse(ApiClient({}).request("POST", "api/emails/1/blocks"))

        assert response.is_idempotent_replay is False

    def test_api_response_is_exported_from_the_package(self):
        """Tests that ApiResponse is available as mailerlite.ApiResponse"""

        assert mailerlite.ApiResponse is ApiResponse
