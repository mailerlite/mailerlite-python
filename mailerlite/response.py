from __future__ import absolute_import

import copy


class ApiResponse(dict):
    """
    The decoded JSON body of a response

    It is a dict, so you use it like the dicts that the other methods return.
    It also has the status code and the headers of the response.
    A response without a body, for example `204`, is an empty dict.
    """

    def __init__(self, response):
        super().__init__(_json_object(response))
        self.status_code = response.status_code
        self.headers = response.headers

    def copy(self):
        """A shallow copy that keeps the status code and the headers"""

        return copy.copy(self)

    @property
    def is_idempotent_replay(self):
        """
        True if the API returned the stored response of an earlier request
        with the same idempotency key
        """

        # A proxy can change the case of the value
        value = self.headers.get("Idempotent-Replayed", "")
        return value.strip().lower() == "true"


def _json_object(response):
    if not response.content:
        return {}

    body = response.json()
    if not isinstance(body, dict):
        raise TypeError(
            f"The API returned a JSON {type(body).__name__}, not a JSON object, "
            f"with status {response.status_code} for url: {response.url}"
        )

    return body
