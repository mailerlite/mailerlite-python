import pytest
import mailerlite
from mailerlite import Client
from mailerlite.exceptions import ApiError, EmptyEtagError, EmptyIdError, InvalidIdError
from mailerlite.response import ApiResponse
from mailerlite.sdk.emails import VERSION_CONFLICT, BlockPosition, BlockType

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

    def test_create_block_inserts_the_block(self, client, mock_api):
        mock_api.add_response(201, load_fixture("email_block_created.json"))
        editor_content = {
            "attrs": {"textAlign": "center"},
            "content": [{"text": "Hi", "type": "text"}],
        }

        response = client.emails.create_block(
            "123", "42", BlockType.PARAGRAPH, editor_content
        )

        assert mock_api.last_request.method == "POST"
        assert mock_api.last_request.url == f"{BASE_URL}/123/blocks"
        assert mock_api.last_body == {
            "type": "paragraph",
            "editor_content": editor_content,
            "etag": "42",
        }
        assert response.status_code == 201
        assert response["etag"] == "43"
        assert response["data"]["id"] == "58"
        assert response["data"]["editor_content"]["attrs"] == {"textAlign": "center"}
        assert response["data"]["placement"] == {"after": "57", "before": None}

    def test_create_block_sends_the_placement(self, client, mock_api):
        mock_api.add_response(201, load_fixture("email_block_created.json"))

        client.emails.create_block(
            "123",
            "42",
            BlockType.DIVIDER,
            {},
            placement={"position": BlockPosition.AFTER, "block_id": "57"},
        )

        assert mock_api.last_body == {
            "type": "divider",
            "editor_content": {},
            "placement": {"position": "after", "block_id": "57"},
            "etag": "42",
        }

    @pytest.mark.parametrize("etag", ["", None])
    def test_create_block_rejects_an_empty_etag(self, client, mock_api, etag):
        with pytest.raises(EmptyEtagError):
            client.emails.create_block("123", etag, BlockType.DIVIDER, {})

        assert mock_api.requests == []

    @pytest.mark.parametrize(
        "etag, editor_content, placement",
        [
            (42, {}, None),
            ("42", None, None),
            ("42", "text", None),
            ("42", {}, "end"),
        ],
    )
    def test_create_block_rejects_arguments_of_the_wrong_type(
        self, client, mock_api, etag, editor_content, placement
    ):
        with pytest.raises(TypeError):
            client.emails.create_block(
                "123", etag, BlockType.DIVIDER, editor_content, placement=placement
            )

        assert mock_api.requests == []

    def test_create_block_rejects_an_invalid_email_id(self, client, mock_api):
        with pytest.raises(InvalidIdError):
            client.emails.create_block("123/html", "42", BlockType.DIVIDER, {})

        assert mock_api.requests == []

    def test_write_with_an_old_etag_raises_a_version_conflict(self, client, mock_api):
        mock_api.add_response(
            409,
            {
                "message": "The email has changed since you read it.",
                "code": "version_conflict",
                "etag": "44",
            },
        )

        with pytest.raises(ApiError) as error:
            client.emails.create_block("123", "42", BlockType.DIVIDER, {})

        assert error.value.status_code == 409
        assert error.value.code == VERSION_CONFLICT
        assert error.value.etag == "44"
        assert "version_conflict" in str(error.value)

    def test_block_constants(self):
        assert BlockType.BLOCKQUOTE == "blockquote"
        assert BlockType.BULLETED_LIST == "bulleted_list"
        assert BlockType.BUTTON == "button"
        assert BlockType.CODE == "code"
        assert BlockType.DIVIDER == "divider"
        assert BlockType.HEADING == "heading"
        assert BlockType.IMAGE == "image"
        assert BlockType.NUMBERED_LIST == "numbered_list"
        assert BlockType.PARAGRAPH == "paragraph"
        assert BlockType.SOCIAL_ICON == "social_icon"
        assert BlockType.TITLE == "title"
        assert BlockType.VIDEO == "video"
        assert BlockPosition.START == "start"
        assert BlockPosition.END == "end"
        assert BlockPosition.BEFORE == "before"
        assert BlockPosition.AFTER == "after"
        assert VERSION_CONFLICT == "version_conflict"

    def test_write_names_are_exported_from_the_package(self):
        assert mailerlite.EmptyEtagError is EmptyEtagError
        assert mailerlite.BlockType is BlockType
        assert mailerlite.BlockPosition is BlockPosition
        assert mailerlite.VERSION_CONFLICT == VERSION_CONFLICT
