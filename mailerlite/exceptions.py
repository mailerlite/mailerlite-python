from __future__ import absolute_import

import requests


class ApiError(requests.HTTPError):
    """
    The API returned a 4xx or 5xx status code

    It is a `requests.HTTPError`, so `e.response` gives the full response.
    The fields are `None` when the response body does not have them.
    """

    def __init__(self, response):
        self.status_code = response.status_code

        body = _json_or_none(response)
        if not isinstance(body, dict):
            body = {}

        self.message = body.get("message")
        self.code = body.get("code")
        self.etag = body.get("etag")
        self.errors = body.get("errors")

        kind = "Client Error" if response.status_code < 500 else "Server Error"
        text = (
            f"{response.status_code} {kind}: {response.reason} for url: {response.url}"
        )
        if self.message:
            detail = f"{self.code}: {self.message}" if self.code else self.message
            text = f"{text} ({detail})"

        super().__init__(text, response=response)

    def __reduce__(self):
        # pickle calls cls(*self.args) by default, but __init__ needs the response
        return self.__class__, (self.response,)


def _json_or_none(response):
    try:
        return response.json()
    except ValueError:
        return None


class EmptyIdError(ValueError):
    """An ID for the URL path is empty. The SDK sends no request."""


class InvalidIdError(ValueError):
    """An ID for the URL path does not contain only digits. The SDK sends no request."""
