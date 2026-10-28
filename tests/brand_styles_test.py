import pytest
from mailerlite import Client
from mailerlite.response import ApiResponse

from tests.conftest import load_fixture

URL = "https://connect.mailerlite.com/api/brand-styles"


@pytest.fixture
def client():
    return Client({"api_key": "1234567890"})


class TestBrandStyles:
    def test_api_url_is_properly_set(self, client):
        assert client.brand_styles.base_api_url == "api/brand-styles"

    def test_get_returns_the_palettes(self, client, mock_api):
        mock_api.add_response(200, load_fixture("brand_styles.json"))

        response = client.brand_styles.get()

        assert mock_api.last_request.method == "GET"
        assert mock_api.last_request.url == URL
        assert mock_api.last_body is None
        assert isinstance(response, ApiResponse)
        data = response["data"]
        assert data["brand"]["identifier"] == "account"
        assert data["brand"]["primary_color"] == "#2cb191"
        assert data["default"]["identifier"] == "default-brand"
        assert [preset["identifier"] for preset in data["presets"]] == [
            "preset-business-casual",
            "preset-retro",
        ]
        assert data["presets"][1]["font_family"] == "Courier New, monospace"

    def test_get_returns_no_brand_when_the_account_has_none(self, client, mock_api):
        body = load_fixture("brand_styles.json")
        body["data"]["brand"] = None
        mock_api.add_response(200, body)

        response = client.brand_styles.get()

        assert response["data"]["brand"] is None
        assert response["data"]["default"]["identifier"] == "default-brand"
