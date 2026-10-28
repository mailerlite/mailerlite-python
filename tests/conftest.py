import json
from http.client import responses
from pathlib import Path

import pytest
import requests

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def pytest_configure():
    return {"entity_id": 0, "entity_email": "random@mailerlite.com"}


def load_fixture(name):
    """Returns the decoded JSON of a file in tests/fixtures"""

    with open(FIXTURES_DIR / name) as fd:
        return json.load(fd)


class MockApi(object):
    """Records the prepared requests and returns the queued responses"""

    def __init__(self):
        self.requests = []
        self.responses = []

    def add_response(self, status_code=200, body=None, headers=None):
        """Queues a response. A dict or list body is encoded as JSON."""

        if isinstance(body, (dict, list)):
            body = json.dumps(body)
        if isinstance(body, str):
            body = body.encode()

        self.responses.append((status_code, body or b"", headers or {}))

    def send(self, request):
        self.requests.append(request)
        status_code, body, headers = self.responses.pop(0)

        response = requests.Response()
        response.status_code = status_code
        response.reason = responses.get(status_code, "")
        response.headers.update({"Content-Type": "application/json", **headers})
        response._content = body
        response.url = request.url
        response.request = request

        return response

    @property
    def last_request(self):
        return self.requests[-1]

    @property
    def last_body(self):
        """Returns the decoded JSON body of the last request, or None without a body"""

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
