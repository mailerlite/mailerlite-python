import json
from types import SimpleNamespace

import pytest
from mailerlite.api_client import ApiClient


def pytest_configure():
    return {"entity_id": 0, "entity_email": "random@mailerlite.com"}


@pytest.fixture
def sent_request(mocker):
    response = mocker.Mock()
    response.json.return_value = {"data": {}}
    request = mocker.patch(
        "mailerlite.api_client.requests.request", return_value=response
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
