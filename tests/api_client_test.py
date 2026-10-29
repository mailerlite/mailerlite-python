import pickle

import pytest
import requests
from mailerlite.api_client import ApiClient
from mailerlite.exceptions import ApiError


class TestApiClient:
    def test_config_api_key_is_set_properly(self):
        """Tests if API key is properly set in configuration"""

        config = {"api_key": "1234567890"}
        client = ApiClient(config)

        assert client.api_key == config["api_key"]
        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == "Bearer " + config["api_key"]

    def test_config_api_version_is_set_properly(self):
        """Tets if API version is properly set in configuration"""

        config = {"api_version": "2038-01-19"}
        client = ApiClient(config)

        assert client.api_version == config["api_version"]
        assert "X-Version" in client.headers
        assert client.headers["X-Version"] == config["api_version"]

        config = {}
        client = ApiClient(config)

        assert "X-Version" not in client.headers

    def test_config_default_headers_are_set_properly(self):
        """Tests if default headers are properly set in configuration"""

        config = {}
        client = ApiClient(config)

        assert type(client.headers) == dict
        assert "Content-Type" in client.headers
        assert "Accept" in client.headers
        assert "User-Agent" in client.headers

        assert client.headers["Content-Type"] == "application/json"
        assert client.headers["Accept"] == "application/json"
        assert client.headers["User-Agent"] == "MailerLite-Python-SDK-Client"

    def test_it_will_return_error_if_request_method_is_not_supported(self):
        """Tests if error is going to be returned in case of incorrect http method"""

        client = ApiClient({})
        with pytest.raises(ValueError):
            client.request("PPOST", "some-url")

    def test_mock_api_records_the_prepared_request(self, mock_api):
        """Tests that mock_api records the request and returns the queued response"""

        mock_api.add_response(200, {"data": []})
        client = ApiClient({"api_key": "1234567890"})

        response = client.request("GET", "api/timezones", {"filter[name]": "a b"})

        assert response.json() == {"data": []}
        assert len(mock_api.requests) == 1
        assert mock_api.last_request.method == "GET"
        assert (
            mock_api.last_request.url
            == "https://connect.mailerlite.com/api/timezones?filter%5Bname%5D=a+b"
        )
        assert mock_api.last_request.headers["Authorization"] == "Bearer 1234567890"
        assert mock_api.last_body is None

    def test_patch_request_sends_the_json_body(self, mock_api):
        """Tests that a PATCH request sends the body as JSON"""

        mock_api.add_response(200, {"data": {}})
        client = ApiClient({})

        client.request("PATCH", "api/emails/1/settings", body={"etag": "42"})

        assert mock_api.last_request.method == "PATCH"
        assert mock_api.last_body == {"etag": "42"}

    def test_delete_request_sends_the_json_body(self, mock_api):
        """Tests that a DELETE request with a body sends the body as JSON"""

        mock_api.add_response(200, {"etag": "43"})
        client = ApiClient({})

        client.request("DELETE", "api/emails/1/blocks/2", body={"etag": "42"})

        assert mock_api.last_request.method == "DELETE"
        assert mock_api.last_body == {"etag": "42"}

    def test_delete_request_without_a_body_sends_no_body(self, mock_api):
        """Tests that a DELETE request without a body sends no body"""

        mock_api.add_response(204)
        client = ApiClient({})

        client.request("DELETE", "api/groups/1")

        assert mock_api.last_request.method == "DELETE"
        assert mock_api.last_request.body is None

    @pytest.mark.parametrize("method", ["POST", "PUT", "PATCH"])
    def test_write_request_without_a_body_sends_no_body(self, mock_api, method):
        """Tests that a write request without a body does not send the JSON `null`"""

        mock_api.add_response(200, {"data": {}})
        client = ApiClient({})

        client.request(method, "api/emails/1/versions")

        assert mock_api.last_request.method == method
        assert mock_api.last_request.body is None

    def test_version_conflict_raises_api_error_with_code_and_etag(self, mock_api):
        """Tests that a 409 response gives the message, the code and the etag"""

        mock_api.add_response(
            409,
            {
                "message": "The email changed. Get it again.",
                "code": "version_conflict",
                "etag": "44",
            },
        )
        client = ApiClient({})

        with pytest.raises(ApiError) as error:
            client.request("PATCH", "api/emails/1/blocks/2", body={"etag": "42"})

        assert isinstance(error.value, requests.HTTPError)
        assert error.value.response.status_code == 409
        assert error.value.status_code == 409
        assert error.value.message == "The email changed. Get it again."
        assert error.value.code == "version_conflict"
        assert error.value.etag == "44"
        assert error.value.errors is None
        assert str(error.value) == (
            "409 Client Error: Conflict for url: "
            "https://connect.mailerlite.com/api/emails/1/blocks/2 "
            "(version_conflict: The email changed. Get it again.)"
        )

    def test_validation_error_raises_api_error_with_errors(self, mock_api):
        """Tests that a 422 response gives the field errors"""

        mock_api.add_response(
            422,
            {
                "message": "The type field is required.",
                "errors": {"type": ["The type field is required."]},
            },
        )
        client = ApiClient({})

        with pytest.raises(ApiError) as error:
            client.request("POST", "api/emails/1/blocks", body={})

        assert error.value.message == "The type field is required."
        assert error.value.code is None
        assert error.value.etag is None
        assert error.value.errors == {"type": ["The type field is required."]}
        # The reason phrase of 422 depends on the Python version
        reason = error.value.response.reason
        assert str(error.value) == (
            f"422 Client Error: {reason} for url: "
            "https://connect.mailerlite.com/api/emails/1/blocks "
            "(The type field is required.)"
        )

    def test_error_without_a_json_body_raises_api_error(self, mock_api):
        """Tests that a response that is not JSON gives an error without details"""

        mock_api.add_response(503, "Service Unavailable", {"Content-Type": "text/html"})
        client = ApiClient({})

        with pytest.raises(ApiError) as error:
            client.request("GET", "api/emails/1/html")

        assert error.value.status_code == 503
        assert error.value.message is None
        assert error.value.code is None
        assert error.value.etag is None
        assert error.value.errors is None
        assert str(error.value) == (
            "503 Server Error: Service Unavailable for url: "
            "https://connect.mailerlite.com/api/emails/1/html"
        )

    def test_api_error_survives_a_pickle_round_trip(self, mock_api):
        """Tests that an ApiError can go to another process, as in multiprocessing"""

        mock_api.add_response(
            409,
            {
                "message": "The email changed. Get it again.",
                "code": "version_conflict",
                "etag": "44",
            },
        )
        client = ApiClient({})

        with pytest.raises(ApiError) as error:
            client.request("PATCH", "api/emails/1/blocks/2", body={"etag": "42"})

        copy = pickle.loads(pickle.dumps(error.value))

        assert isinstance(copy, ApiError)
        assert str(copy) == str(error.value)
        assert copy.status_code == 409
        assert copy.message == "The email changed. Get it again."
        assert copy.code == "version_conflict"
        assert copy.etag == "44"
        assert copy.errors is None
        assert copy.response.status_code == 409

    def test_api_error_is_exported_from_the_package(self):
        """Tests that ApiError is available as mailerlite.ApiError"""

        import mailerlite

        assert mailerlite.ApiError is ApiError

    def test_request_adds_the_given_headers(self, mock_api):
        """Tests that request() sends extra headers only for that request"""

        mock_api.add_response(200, {"data": {}})
        mock_api.add_response(200, {"data": {}})
        client = ApiClient({"api_key": "1234567890"})

        client.request(
            "POST", "api/emails/1/versions", headers={"Idempotency-Key": "k1"}
        )
        assert mock_api.last_request.headers["Idempotency-Key"] == "k1"
        assert mock_api.last_request.headers["Authorization"] == "Bearer 1234567890"

        client.request("POST", "api/emails/1/versions")
        assert "Idempotency-Key" not in mock_api.last_request.headers
        assert "Idempotency-Key" not in client.headers
