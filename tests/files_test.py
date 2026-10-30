import pytest
import mailerlite
from mailerlite import Client
from mailerlite.response import ApiResponse
from mailerlite.sdk.files import FileSort, FileType

from tests.conftest import load_fixture

URL = "https://connect.mailerlite.com/api/files"


@pytest.fixture
def client():
    return Client({"api_key": "1234567890"})


class TestFiles:
    def test_api_url_is_properly_set(self, client):
        assert client.files.base_api_url == "api/files"

    def test_list_without_options(self, client, mock_api):
        mock_api.add_response(200, load_fixture("files.json"))

        response = client.files.list()

        assert mock_api.last_request.method == "GET"
        assert mock_api.last_request.url == URL
        assert mock_api.last_body is None
        assert isinstance(response, ApiResponse)
        image, pdf = response["data"]
        assert image["id"] == "301"
        assert image["type"] == "image"
        assert image["name"] == "summer sale banner.png"
        assert image["size"] == 48213
        assert (image["width"], image["height"]) == (1200, 600)
        assert pdf["type"] == "pdf"
        assert pdf["width"] is None
        assert pdf["height"] is None
        assert response["meta"]["total"] == 2

    def test_list_sends_a_name_filter_with_spaces(self, client, mock_api):
        mock_api.add_response(200, load_fixture("files.json"))

        client.files.list(filter={"name": "summer sale"})

        assert mock_api.last_request.url == f"{URL}?filter%5Bname%5D=summer+sale"

    def test_list_sends_all_options(self, client, mock_api):
        mock_api.add_response(200, load_fixture("files.json"))

        client.files.list(
            filter={"name": "banner", "type": FileType.IMAGE},
            sort=FileSort.SIZE_DESCENDING,
            page=2,
            limit=50,
        )

        assert mock_api.last_request.url == (
            f"{URL}?filter%5Bname%5D=banner&filter%5Btype%5D=image"
            "&sort=-size&page=2&limit=50"
        )

    def test_list_rejects_a_filter_of_the_wrong_type(self, client, mock_api):
        with pytest.raises(TypeError):
            client.files.list(filter="image")

        assert mock_api.requests == []

    def test_file_constants(self):
        assert FileType.IMAGE == "image"
        assert FileType.PDF == "pdf"
        assert FileType.EPUB == "epub"
        assert FileSort.CREATED_AT == "created_at"
        assert FileSort.CREATED_AT_DESCENDING == "-created_at"
        assert FileSort.NAME == "name"
        assert FileSort.NAME_DESCENDING == "-name"
        assert FileSort.SIZE == "size"
        assert FileSort.SIZE_DESCENDING == "-size"
        assert mailerlite.FileType is FileType
        assert mailerlite.FileSort is FileSort
