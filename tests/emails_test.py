import pytest
from mailerlite import Client
from mailerlite.exceptions import EmptyIdError, InvalidIdError
from mailerlite.response import ApiResponse

from tests.conftest import load_fixture

BASE_URL = "https://connect.mailerlite.com/api/emails"


@pytest.fixture
def client():
    return Client({"api_key": "1234567890"})


class TestEmails:
    def test_api_url_is_properly_set(self, client):
        assert client.emails.base_api_url == "api/emails"

    def test_get_returns_the_email(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email.json"))

        response = client.emails.get("123")

        assert mock_api.last_request.method == "GET"
        assert mock_api.last_request.url == f"{BASE_URL}/123"
        assert mock_api.last_body is None
        assert isinstance(response, ApiResponse)
        assert response.status_code == 200
        assert response["etag"] == "42"
        email = response["data"]
        assert email["id"] == "123"
        assert email["type"] == "builder_inline_email"
        assert email["emailable_type"] == "campaigns"
        assert email["emailable_id"] == "456"
        assert email["settings"]["brand"]["mode"] == "account"
        assert email["settings"]["typography"]["heading"]["h1"]["size"] == "32"
        assert email["settings"]["button"]["border_radius"] == "4"
        assert email["settings"]["footer"]["show_preferences"] is False
        assert email["settings"]["footer"]["social_links"][0]["link_id"] == 7
        assert email["blocks"][0]["editor_content"]["attrs"] == {"textAlign": "left"}
        assert email["blocks"][1]["children"][0]["id"] == "3"

    def test_get_accepts_an_int_id(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email.json"))

        client.emails.get(123)

        assert mock_api.last_request.url == f"{BASE_URL}/123"

    @pytest.mark.parametrize("email_id", ["", None])
    def test_get_rejects_an_empty_id(self, client, mock_api, email_id):
        with pytest.raises(EmptyIdError):
            client.emails.get(email_id)

        assert mock_api.requests == []

    @pytest.mark.parametrize(
        "email_id", ["123/html", "123%2Fhtml", "12 3", "-1", "²", "123\n", "abc"]
    )
    def test_get_rejects_an_id_that_is_not_only_digits(
        self, client, mock_api, email_id
    ):
        with pytest.raises(InvalidIdError):
            client.emails.get(email_id)

        assert mock_api.requests == []

    @pytest.mark.parametrize("email_id", [True, 1.5, ["123"]])
    def test_get_rejects_an_id_of_the_wrong_type(self, client, mock_api, email_id):
        with pytest.raises(TypeError):
            client.emails.get(email_id)

        assert mock_api.requests == []

    def test_id_errors_are_value_errors(self):
        assert issubclass(EmptyIdError, ValueError)
        assert issubclass(InvalidIdError, ValueError)

    def test_get_html_returns_the_html(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email_html.json"))

        response = client.emails.get_html("123")

        assert mock_api.last_request.method == "GET"
        assert mock_api.last_request.url == f"{BASE_URL}/123/html"
        assert mock_api.last_body is None
        assert response["data"]["html"] == (
            "<!doctype html><html><body><p>Hello</p></body></html>"
        )
        assert response["etag"] == "42"

    def test_get_html_rejects_an_invalid_id(self, client, mock_api):
        with pytest.raises(InvalidIdError):
            client.emails.get_html("123/blocks")

        assert mock_api.requests == []

    def test_get_block_returns_the_block(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email_block.json"))

        response = client.emails.get_block("123", "57")

        assert mock_api.last_request.method == "GET"
        assert mock_api.last_request.url == f"{BASE_URL}/123/blocks/57"
        assert mock_api.last_body is None
        assert response["etag"] == "43"
        block = response["data"]
        assert block["id"] == "57"
        assert block["type"] == "paragraph"
        assert block["editor_content"]["attrs"] == {"textAlign": "left"}
        assert block["placement"] == {"after": "56", "before": None}

    @pytest.mark.parametrize(
        "email_id, block_id, error",
        [
            ("", "57", EmptyIdError),
            ("123", "", EmptyIdError),
            ("123", None, EmptyIdError),
            ("123/html", "57", InvalidIdError),
            ("123", "57/move", InvalidIdError),
        ],
    )
    def test_get_block_rejects_an_invalid_id(
        self, client, mock_api, email_id, block_id, error
    ):
        with pytest.raises(error):
            client.emails.get_block(email_id, block_id)

        assert mock_api.requests == []
