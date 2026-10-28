from __future__ import absolute_import

import re

from mailerlite.exceptions import EmptyIdError, InvalidIdError
from mailerlite.response import ApiResponse

_ID_PATTERN = re.compile(r"[0-9]+")


class Emails(object):
    """
    Emails built with the simple editor

    To create such an email, create a campaign with `"editor": "simple"`.
    IDs are strings of digits. You can also give them as int.
    """

    # Emails base API uri
    base_api_url = "api/emails"

    def __init__(self, api_client):
        self.api_client = api_client

    def get(self, email_id):
        """
        Get an email

        Returns the email with its settings and blocks, and the etag of the email.

        :param email_id: str|int Email ID
        :raises: :class: `TypeError` : `email_id` type is not valid
        :raises: :class: `EmptyIdError` : `email_id` is empty
        :raises: :class: `InvalidIdError` : `email_id` does not contain only digits
        :raises: :class: `ApiError` : API request failed, e.g. email was not found
        :return: JSON object
        :rtype: ApiResponse
        """

        email_id = _path_id(email_id, "email_id")

        return ApiResponse(
            self.api_client.request("GET", f"{self.base_api_url}/{email_id}")
        )


def _path_id(value, name):
    """Returns the ID as a string for the URL path, or raises if it is not valid"""

    if value is None or value == "":
        raise EmptyIdError(f"`{name}` must not be empty.")

    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise TypeError(
            f"`{name}` type is not valid. Expected `str` or `int`, got {type(value)}."
        )

    value = str(value)
    # fullmatch, because `$` also matches before a final new line,
    # and str.isdigit() also accepts digits that are not ASCII.
    if not _ID_PATTERN.fullmatch(value):
        raise InvalidIdError(f"`{name}` must contain only digits, got {value!r}.")

    return value
