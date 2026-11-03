import json
from http.client import responses
from pathlib import Path
from types import SimpleNamespace

import pytest
import requests
from mailerlite.api_client import ApiClient

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def pytest_configure():
    return {"entity_id": 0, "entity_email": "random@mailerlite.com"}


def load_fixture(name):
    with open(FIXTURES_DIR / name) as fd:
        return json.load(fd)


def make_response(status_code=200, body=b"", headers=None, url=None, request=None):
    """A real requests.Response, so the client can check its status code."""

    response = requests.Response()
    response.status_code = status_code
    response.reason = responses.get(status_code, "")
    response.headers.update({"Content-Type": "application/json", **(headers or {})})
    response._content = body
    response.url = url
    response.request = request

    return response


class MockApi(object):
    def __init__(self):
        self.requests = []
        self.responses = []

    def add_response(self, status_code=200, body=None, headers=None):
        if isinstance(body, (dict, list)):
            body = json.dumps(body)
        if isinstance(body, str):
            body = body.encode()

        self.responses.append((status_code, body or b"", headers or {}))

    def send(self, request):
        self.requests.append(request)
        status_code, body, headers = self.responses.pop(0)

        return make_response(status_code, body, headers, request.url, request)

    @property
    def last_request(self):
        return self.requests[-1]

    @property
    def last_body(self):
        body = self.last_request.body
        return None if body is None else json.loads(body)


@pytest.fixture
def mock_api(mocker):
    """Replaces the HTTP transport. No request leaves the machine."""

    api = MockApi()
    mocker.patch(
        "requests.Session.send",
        autospec=True,
        side_effect=lambda session, request, **kwargs: api.send(request),
    )

    return api


@pytest.fixture
def sent_request(mocker):
    """Replaces requests.request and gives back the method, path, params and body"""

    def respond(**kwargs):
        return make_response(200, b'{"data": {}}', url=kwargs["url"])

    request = mocker.patch(
        "mailerlite.api_client.requests.request", side_effect=respond
    )

    def last_request():
        kwargs = request.call_args.kwargs
        body = kwargs.get("data")
        return SimpleNamespace(
            method=kwargs["method"].upper(),
            path=kwargs["url"].removeprefix(ApiClient.HOST + "api"),
            params=kwargs["params"],
            body=json.loads(body) if body else None,
        )

    return last_request
