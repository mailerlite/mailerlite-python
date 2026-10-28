from __future__ import absolute_import

import re

from mailerlite.exceptions import EmptyEtagError, EmptyIdError, InvalidIdError
from mailerlite.response import ApiResponse

_ID_PATTERN = re.compile(r"[0-9]+")

# The error code of a write with an etag that is not the current etag of the email
VERSION_CONFLICT = "version_conflict"


class BlockType(object):
    """Block types. The API can also return types that are not in this list."""

    BLOCKQUOTE = "blockquote"
    BULLETED_LIST = "bulleted_list"
    BUTTON = "button"
    CODE = "code"
    DIVIDER = "divider"
    HEADING = "heading"
    IMAGE = "image"
    NUMBERED_LIST = "numbered_list"
    PARAGRAPH = "paragraph"
    SOCIAL_ICON = "social_icon"
    # Only reads return this type. You cannot insert a block of this type.
    TITLE = "title"
    VIDEO = "video"


class BlockPosition(object):
    """Positions of a block. `BEFORE` and `AFTER` also need a `block_id`."""

    START = "start"
    END = "end"
    BEFORE = "before"
    AFTER = "after"


class BrandMode(object):
    """Where the palette of an email comes from, in `settings["brand"]["mode"]`"""

    ACCOUNT = "account"
    TEMPLATE = "template"
    CUSTOM = "custom"


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

    def get_html(self, email_id):
        """
        Get the HTML of an email

        Returns the HTML that the email sends, and the etag of the email.
        The API can return a temporary `503` error.

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
            self.api_client.request("GET", f"{self.base_api_url}/{email_id}/html")
        )

    def get_block(self, email_id, block_id):
        """
        Get a block of an email

        Returns the block, its place in the email, and the etag of the email.

        :param email_id: str|int Email ID
        :param block_id: str|int Block ID
        :raises: :class: `TypeError` : `email_id` or `block_id` type is not valid
        :raises: :class: `EmptyIdError` : `email_id` or `block_id` is empty
        :raises: :class: `InvalidIdError` : an ID does not contain only digits
        :raises: :class: `ApiError` : API request failed, e.g. block was not found
        :return: JSON object
        :rtype: ApiResponse
        """

        email_id = _path_id(email_id, "email_id")
        block_id = _path_id(block_id, "block_id")

        return ApiResponse(
            self.api_client.request(
                "GET", f"{self.base_api_url}/{email_id}/blocks/{block_id}"
            )
        )

    def create_block(self, email_id, etag, block_type, editor_content, placement=None):
        """
        Insert a block in an email

        Returns the new block and the new etag of the email.

        :param email_id: str|int Email ID
        :param etag: str The etag from the last response for this email
        :param block_type: str Block type, see `BlockType`. You cannot insert `title`.
        :param editor_content: dict The content of the block. It can be empty.
            Its keys are camelCase, for example `textAlign`.
        :param placement: dict Optional. `{"position": ..., "block_id": ...}`,
            see `BlockPosition`. Without it, the API puts the block at the end.
        :raises: :class: `TypeError` : an argument type is not valid
        :raises: :class: `EmptyIdError` : `email_id` is empty
        :raises: :class: `InvalidIdError` : `email_id` does not contain only digits
        :raises: :class: `EmptyEtagError` : `etag` is empty
        :raises: :class: `ApiError` : API request failed, e.g. the etag is old
        :return: JSON object
        :rtype: ApiResponse
        """

        email_id = _path_id(email_id, "email_id")
        body = _block_body(block_type, editor_content, placement)
        body["etag"] = _etag(etag)

        return ApiResponse(
            self.api_client.request(
                "POST", f"{self.base_api_url}/{email_id}/blocks", body=body
            )
        )

    def update_block(self, email_id, block_id, etag, editor_content):
        """
        Update a block of an email

        Replaces the whole content of the block. The API removes the keys that you
        do not send. Returns the block and the new etag of the email.

        :param email_id: str|int Email ID
        :param block_id: str|int Block ID
        :param etag: str The etag from the last response for this email
        :param editor_content: dict The new content of the block.
            Its keys are camelCase, for example `textAlign`.
        :raises: :class: `TypeError` : an argument type is not valid
        :raises: :class: `EmptyIdError` : `email_id` or `block_id` is empty
        :raises: :class: `InvalidIdError` : an ID does not contain only digits
        :raises: :class: `EmptyEtagError` : `etag` is empty
        :raises: :class: `ApiError` : API request failed, e.g. the etag is old
        :return: JSON object
        :rtype: ApiResponse
        """

        email_id = _path_id(email_id, "email_id")
        block_id = _path_id(block_id, "block_id")
        _require_dict(editor_content, "editor_content")
        body = {"editor_content": editor_content, "etag": _etag(etag)}

        return ApiResponse(
            self.api_client.request(
                "PATCH", f"{self.base_api_url}/{email_id}/blocks/{block_id}", body=body
            )
        )

    def delete_block(self, email_id, block_id, etag):
        """
        Delete a block of an email

        Also deletes the blocks in it. Returns the new etag of the email,
        so it returns the response and not `True` like the other deletes.

        :param email_id: str|int Email ID
        :param block_id: str|int Block ID
        :param etag: str The etag from the last response for this email
        :raises: :class: `TypeError` : an argument type is not valid
        :raises: :class: `EmptyIdError` : `email_id` or `block_id` is empty
        :raises: :class: `InvalidIdError` : an ID does not contain only digits
        :raises: :class: `EmptyEtagError` : `etag` is empty
        :raises: :class: `ApiError` : API request failed, e.g. the etag is old
        :return: JSON object with only the new etag
        :rtype: ApiResponse
        """

        email_id = _path_id(email_id, "email_id")
        block_id = _path_id(block_id, "block_id")
        body = {"etag": _etag(etag)}

        return ApiResponse(
            self.api_client.request(
                "DELETE", f"{self.base_api_url}/{email_id}/blocks/{block_id}", body=body
            )
        )

    def move_block(self, email_id, block_id, etag, placement):
        """
        Move a block of an email

        Returns the block, its new place in the email, and the new etag of the email.

        :param email_id: str|int Email ID
        :param block_id: str|int Block ID
        :param etag: str The etag from the last response for this email
        :param placement: dict `{"position": ..., "block_id": ...}`, see `BlockPosition`
        :raises: :class: `TypeError` : an argument type is not valid
        :raises: :class: `EmptyIdError` : `email_id` or `block_id` is empty
        :raises: :class: `InvalidIdError` : an ID does not contain only digits
        :raises: :class: `EmptyEtagError` : `etag` is empty
        :raises: :class: `ApiError` : API request failed, e.g. the etag is old
        :return: JSON object
        :rtype: ApiResponse
        """

        email_id = _path_id(email_id, "email_id")
        block_id = _path_id(block_id, "block_id")
        _require_dict(placement, "placement")
        body = {"placement": placement, "etag": _etag(etag)}

        return ApiResponse(
            self.api_client.request(
                "POST",
                f"{self.base_api_url}/{email_id}/blocks/{block_id}/move",
                body=body,
            )
        )

    def validate_block(self, block_type, editor_content, placement=None):
        """
        Validate a block

        Checks a block without an email and without an etag. An invalid block
        is not an error: the response has `valid` set to false and the `errors`.

        :param block_type: str Block type, see `BlockType`
        :param editor_content: dict The content of the block
        :param placement: dict Optional. `{"position": ..., "block_id": ...}`
        :raises: :class: `TypeError` : an argument type is not valid
        :raises: :class: `ApiError` : API request failed
        :return: JSON object with `valid`, `errors` and `schema`
        :rtype: ApiResponse
        """

        body = _block_body(block_type, editor_content, placement)

        return ApiResponse(
            self.api_client.request(
                "POST", f"{self.base_api_url}/blocks/validate", body=body
            )
        )

    def update_settings(self, email_id, etag, settings):
        """
        Update the design settings of an email

        Send only the keys to change, in the shape of `settings` in `get()`.
        The API stores each value that you send, also a value that the email
        inherits from the account. An empty string unsets a value.
        `footer.social_links` replaces the whole list: keep the `link_id` of
        each link to keep its click history.

        The response can have `rejected` when the API removed unsafe values.

        :param email_id: str|int Email ID
        :param etag: str The etag from the last response for this email
        :param settings: dict The settings to change
        :raises: :class: `TypeError` : an argument type is not valid
        :raises: :class: `EmptyIdError` : `email_id` is empty
        :raises: :class: `InvalidIdError` : `email_id` does not contain only digits
        :raises: :class: `EmptyEtagError` : `etag` is empty
        :raises: :class: `ApiError` : API request failed, e.g. the etag is old
        :return: JSON object
        :rtype: ApiResponse
        """

        email_id = _path_id(email_id, "email_id")
        _require_dict(settings, "settings")
        body = {**settings, "etag": _etag(etag)}

        return ApiResponse(
            self.api_client.request(
                "PATCH", f"{self.base_api_url}/{email_id}/settings", body=body
            )
        )

    def validate_settings(self, email_id, settings):
        """
        Validate a change to the design settings of an email

        Checks the settings with the rules of `update_settings()` and saves nothing.
        It needs no etag. Invalid settings are not an error: the response has
        `valid` set to false and the `errors`.

        :param email_id: str|int Email ID
        :param settings: dict The settings that you want to send to `update_settings()`
        :raises: :class: `TypeError` : an argument type is not valid
        :raises: :class: `EmptyIdError` : `email_id` is empty
        :raises: :class: `InvalidIdError` : `email_id` does not contain only digits
        :raises: :class: `ApiError` : API request failed
        :return: JSON object with `valid`, `errors`, `schema` and maybe `rejected`
        :rtype: ApiResponse
        """

        email_id = _path_id(email_id, "email_id")
        _require_dict(settings, "settings")

        return ApiResponse(
            self.api_client.request(
                "POST",
                f"{self.base_api_url}/{email_id}/settings/validate",
                body=settings,
            )
        )

    def create_template(self, email_id, name):
        """
        Save an email as a template

        Copies the email to a new template with the given name.
        The API cannot delete templates.

        :param email_id: str|int Email ID
        :param name: str Name of the template
        :raises: :class: `TypeError` : an argument type is not valid
        :raises: :class: `EmptyIdError` : `email_id` is empty
        :raises: :class: `InvalidIdError` : `email_id` does not contain only digits
        :raises: :class: `ApiError` : API request failed
        :return: JSON object
        :rtype: ApiResponse
        """

        email_id = _path_id(email_id, "email_id")
        if not isinstance(name, str):
            raise TypeError(
                f"`name` type is not valid. Expected `str`, got {type(name)}."
            )

        return ApiResponse(
            self.api_client.request(
                "POST", f"{self.base_api_url}/{email_id}/templates", body={"name": name}
            )
        )

    def list_versions(self, email_id, page=None, limit=None):
        """
        List the versions of an email

        Returns the saved versions, newest first. `current` marks the version
        that the email has now.

        :param email_id: str|int Email ID
        :param page: int Optional. Page number
        :param limit: int Optional. Number of versions on a page
        :raises: :class: `TypeError` : `email_id` type is not valid
        :raises: :class: `EmptyIdError` : `email_id` is empty
        :raises: :class: `InvalidIdError` : `email_id` does not contain only digits
        :raises: :class: `ApiError` : API request failed
        :return: JSON object
        :rtype: ApiResponse
        """

        email_id = _path_id(email_id, "email_id")
        query_params = _without_none({"page": page, "limit": limit})

        return ApiResponse(
            self.api_client.request(
                "GET", f"{self.base_api_url}/{email_id}/versions", query_params
            )
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


def _block_body(block_type, editor_content, placement):
    """Returns the body to insert or to validate a block"""

    _require_dict(editor_content, "editor_content")

    body = {"type": block_type, "editor_content": editor_content}
    if placement is not None:
        _require_dict(placement, "placement")
        body["placement"] = placement

    return body


def _without_none(params):
    """Returns the params without the keys that have no value"""

    return {key: value for key, value in params.items() if value is not None}


def _etag(value):
    """Returns the etag for the body of a write, or raises if it is not valid"""

    if value is None or value == "":
        raise EmptyEtagError("`etag` must not be empty.")

    if not isinstance(value, str):
        raise TypeError(f"`etag` type is not valid. Expected `str`, got {type(value)}.")

    return value


def _require_dict(value, name):
    """Raises if the value is not a dict"""

    if not isinstance(value, dict):
        raise TypeError(
            f"`{name}` type is not valid. Expected `dict`, got {type(value)}."
        )
