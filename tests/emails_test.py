import pytest
import mailerlite
from mailerlite import Client
from mailerlite.exceptions import ApiError, EmptyEtagError, EmptyIdError, InvalidIdError
from mailerlite.response import ApiResponse
from mailerlite.sdk.emails import (
    VERSION_CONFLICT,
    BlockPosition,
    BlockType,
    BrandMode,
)

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

    def test_update_block_replaces_the_editor_content(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email_block_updated.json"))
        editor_content = {"content": [{"text": "Hello again", "type": "text"}]}

        response = client.emails.update_block("123", "57", "43", editor_content)

        assert mock_api.last_request.method == "PATCH"
        assert mock_api.last_request.url == f"{BASE_URL}/123/blocks/57"
        assert mock_api.last_body == {"editor_content": editor_content, "etag": "43"}
        assert response["etag"] == "44"
        assert response["data"]["editor_content"] == editor_content
        assert response["data"]["placement"] == {"after": "56", "before": "58"}

    @pytest.mark.parametrize(
        "block_id, etag, editor_content, error",
        [
            ("", "43", {}, EmptyIdError),
            ("57/move", "43", {}, InvalidIdError),
            ("57", "", {}, EmptyEtagError),
            ("57", "43", None, TypeError),
        ],
    )
    def test_update_block_rejects_invalid_arguments(
        self, client, mock_api, block_id, etag, editor_content, error
    ):
        with pytest.raises(error):
            client.emails.update_block("123", block_id, etag, editor_content)

        assert mock_api.requests == []

    def test_delete_block_sends_the_etag_in_the_body(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email_etag.json"))

        response = client.emails.delete_block("123", "57", "44")

        assert mock_api.last_request.method == "DELETE"
        assert mock_api.last_request.url == f"{BASE_URL}/123/blocks/57"
        assert mock_api.last_body == {"etag": "44"}
        assert response == {"etag": "45"}
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "block_id, etag, error",
        [
            (None, "44", EmptyIdError),
            ("57%2F", "44", InvalidIdError),
            ("57", None, EmptyEtagError),
        ],
    )
    def test_delete_block_rejects_invalid_arguments(
        self, client, mock_api, block_id, etag, error
    ):
        with pytest.raises(error):
            client.emails.delete_block("123", block_id, etag)

        assert mock_api.requests == []

    def test_move_block_sends_the_placement(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email_block_moved.json"))

        response = client.emails.move_block(
            "123", "57", "45", {"position": BlockPosition.START}
        )

        assert mock_api.last_request.method == "POST"
        assert mock_api.last_request.url == f"{BASE_URL}/123/blocks/57/move"
        assert mock_api.last_body == {"placement": {"position": "start"}, "etag": "45"}
        assert response["etag"] == "46"
        assert response["data"]["id"] == "57"
        assert response["data"]["placement"] == {"after": None, "before": "1"}

    @pytest.mark.parametrize(
        "block_id, etag, placement, error",
        [
            ("", "45", {"position": "end"}, EmptyIdError),
            ("57/x", "45", {"position": "end"}, InvalidIdError),
            ("57", "", {"position": "end"}, EmptyEtagError),
            ("57", "45", None, TypeError),
            ("57", "45", "end", TypeError),
        ],
    )
    def test_move_block_rejects_invalid_arguments(
        self, client, mock_api, block_id, etag, placement, error
    ):
        with pytest.raises(error):
            client.emails.move_block("123", block_id, etag, placement)

        assert mock_api.requests == []

    def test_validate_block_sends_the_block_without_an_etag(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email_block_validation_valid.json"))

        response = client.emails.validate_block(
            BlockType.HEADING,
            {"attrs": {"level": 2}},
            placement={"position": BlockPosition.END},
        )

        assert mock_api.last_request.method == "POST"
        assert mock_api.last_request.url == f"{BASE_URL}/blocks/validate"
        assert mock_api.last_body == {
            "type": "heading",
            "editor_content": {"attrs": {"level": 2}},
            "placement": {"position": "end"},
        }
        assert response["valid"] is True
        assert response["errors"] == {}
        assert response["schema"] == {"version": "2.73.2", "hash": "0f3a9c"}

    def test_validate_block_returns_the_errors_of_an_invalid_block(
        self, client, mock_api
    ):
        mock_api.add_response(200, load_fixture("email_block_validation_invalid.json"))

        response = client.emails.validate_block("table", {})

        assert mock_api.last_body == {"type": "table", "editor_content": {}}
        assert response.status_code == 200
        assert response["valid"] is False
        assert response["errors"] == {"type": ["The selected type is invalid."]}

    def test_validate_block_rejects_editor_content_of_the_wrong_type(
        self, client, mock_api
    ):
        with pytest.raises(TypeError):
            client.emails.validate_block(BlockType.HEADING, [])

        assert mock_api.requests == []

    def test_update_settings_sends_only_the_given_keys(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email_settings.json"))
        settings = {
            "brand": {"mode": BrandMode.CUSTOM, "background_color": "#f4f4f4"},
            "footer": {"info_text": {"editor_content": {"content": []}}},
            "typography": {"link": {"color": ""}},
        }

        response = client.emails.update_settings("123", "46", settings)

        assert mock_api.last_request.method == "PATCH"
        assert mock_api.last_request.url == f"{BASE_URL}/123/settings"
        assert mock_api.last_body == {
            "brand": {"mode": "custom", "background_color": "#f4f4f4"},
            "footer": {"info_text": {"editor_content": {"content": []}}},
            "typography": {"link": {"color": ""}},
            "etag": "46",
        }
        assert response["etag"] == "47"
        assert response["data"]["brand"]["mode"] == "custom"
        assert response["data"]["brand"]["background_color"] == "#f4f4f4"
        assert response["data"]["footer"]["social_links"][0]["link_id"] == 7
        assert response["rejected"] == {
            "message": "Some attributes were rejected.",
            "keys": ["footer.social_links[0].url"],
        }

    def test_update_settings_does_not_change_the_given_dict(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email_settings.json"))
        settings = {"layout": {"alignment": "left"}}

        client.emails.update_settings("123", "46", settings)

        assert settings == {"layout": {"alignment": "left"}}

    @pytest.mark.parametrize(
        "email_id, etag, settings, error",
        [
            ("", "46", {}, EmptyIdError),
            ("123/html", "46", {}, InvalidIdError),
            ("123", "", {}, EmptyEtagError),
            ("123", "46", None, TypeError),
        ],
    )
    def test_update_settings_rejects_invalid_arguments(
        self, client, mock_api, email_id, etag, settings, error
    ):
        with pytest.raises(error):
            client.emails.update_settings(email_id, etag, settings)

        assert mock_api.requests == []

    def test_brand_mode_constants(self):
        assert BrandMode.ACCOUNT == "account"
        assert BrandMode.TEMPLATE == "template"
        assert BrandMode.CUSTOM == "custom"
        assert mailerlite.BrandMode is BrandMode

    def test_validate_settings_sends_the_settings_without_an_etag(
        self, client, mock_api
    ):
        mock_api.add_response(200, load_fixture("email_settings_validation.json"))

        response = client.emails.validate_settings("123", {"layout": {"width": "700"}})

        assert mock_api.last_request.method == "POST"
        assert mock_api.last_request.url == f"{BASE_URL}/123/settings/validate"
        assert mock_api.last_body == {"layout": {"width": "700"}}
        assert response.status_code == 200
        assert response["valid"] is False
        assert response["errors"] == {
            "layout.width": ["The layout.width field cannot be changed."]
        }
        assert response["schema"]["version"] == "2.73.2"
        assert response["rejected"]["keys"] == ["footer.social_links[0].url"]

    @pytest.mark.parametrize(
        "email_id, settings, error",
        [
            (None, {}, EmptyIdError),
            ("1.5", {}, InvalidIdError),
            ("123", [], TypeError),
        ],
    )
    def test_validate_settings_rejects_invalid_arguments(
        self, client, mock_api, email_id, settings, error
    ):
        with pytest.raises(error):
            client.emails.validate_settings(email_id, settings)

        assert mock_api.requests == []

    def test_create_template_saves_the_email_as_a_template(self, client, mock_api):
        mock_api.add_response(201, load_fixture("email_template.json"))

        response = client.emails.create_template("123", "Newsletter")

        assert mock_api.last_request.method == "POST"
        assert mock_api.last_request.url == f"{BASE_URL}/123/templates"
        assert mock_api.last_body == {"name": "Newsletter"}
        assert response.status_code == 201
        assert response["data"] == {
            "id": "789",
            "name": "Newsletter",
            "type": "email",
            "created_at": "2026-10-28 12:00:00",
        }
        assert "etag" not in response

    @pytest.mark.parametrize(
        "email_id, name, error",
        [
            ("", "Newsletter", EmptyIdError),
            ("12a", "Newsletter", InvalidIdError),
            ("123", None, TypeError),
        ],
    )
    def test_create_template_rejects_invalid_arguments(
        self, client, mock_api, email_id, name, error
    ):
        with pytest.raises(error):
            client.emails.create_template(email_id, name)

        assert mock_api.requests == []

    def test_list_versions_without_options(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email_versions.json"))

        response = client.emails.list_versions("123")

        assert mock_api.last_request.method == "GET"
        assert mock_api.last_request.url == f"{BASE_URL}/123/versions"
        assert mock_api.last_body is None
        assert response["data"][0] == {
            "id": "902",
            "created_at": "2026-10-28 12:05:00",
            "current": True,
        }
        assert response["data"][1]["current"] is False
        assert response["links"]["next"] is None
        assert response["meta"]["total"] == 2
        assert "etag" not in response

    def test_list_versions_sends_the_page_and_the_limit(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email_versions.json"))

        client.emails.list_versions("123", page=2, limit=10)

        assert mock_api.last_request.url == f"{BASE_URL}/123/versions?page=2&limit=10"

    def test_list_versions_rejects_an_invalid_id(self, client, mock_api):
        with pytest.raises(InvalidIdError):
            client.emails.list_versions("123/blocks")

        assert mock_api.requests == []

    @pytest.mark.parametrize("status_code", [201, 200])
    def test_create_version_returns_the_version(self, client, mock_api, status_code):
        mock_api.add_response(status_code, load_fixture("email_version.json"))

        response = client.emails.create_version("123")

        assert mock_api.last_request.method == "POST"
        assert mock_api.last_request.url == f"{BASE_URL}/123/versions"
        assert mock_api.last_body is None
        assert response.status_code == status_code
        assert response["data"] == {
            "id": "903",
            "created_at": "2026-10-28 12:10:00",
            "current": True,
        }
        assert "etag" not in response

    def test_create_version_rejects_an_empty_id(self, client, mock_api):
        with pytest.raises(EmptyIdError):
            client.emails.create_version("")

        assert mock_api.requests == []

    def test_restore_version_returns_the_email(self, client, mock_api):
        mock_api.add_response(200, load_fixture("email.json"))

        response = client.emails.restore_version("123", "901", "47")

        assert mock_api.last_request.method == "POST"
        assert mock_api.last_request.url == f"{BASE_URL}/123/versions/901/restore"
        assert mock_api.last_body == {"etag": "47"}
        assert response["etag"] == "42"
        assert response["data"]["id"] == "123"
        assert response["data"]["blocks"][0]["id"] == "1"

    @pytest.mark.parametrize(
        "version_id, etag, error",
        [
            ("", "47", EmptyIdError),
            ("901/restore", "47", InvalidIdError),
            ("901", "", EmptyEtagError),
            ("901", 47, TypeError),
        ],
    )
    def test_restore_version_rejects_invalid_arguments(
        self, client, mock_api, version_id, etag, error
    ):
        with pytest.raises(error):
            client.emails.restore_version("123", version_id, etag)

        assert mock_api.requests == []
