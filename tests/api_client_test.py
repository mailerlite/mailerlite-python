import pytest
from mailerlite.api_client import ApiClient


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
