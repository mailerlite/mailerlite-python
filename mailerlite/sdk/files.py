from __future__ import absolute_import

from mailerlite.response import ApiResponse
from mailerlite.sdk import _params


class FileType(object):
    """File types for `filter={"type": ...}`"""

    IMAGE = "image"
    PDF = "pdf"
    EPUB = "epub"


class FileSort(object):
    """Sort values. The values that start with `-` sort in descending order."""

    CREATED_AT = "created_at"
    CREATED_AT_DESCENDING = "-created_at"
    NAME = "name"
    NAME_DESCENDING = "-name"
    SIZE = "size"
    SIZE_DESCENDING = "-size"


class Files(object):
    # Files base API uri
    base_api_url = "api/files"

    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, filter=None, sort=None, page=None, limit=None):
        """
        List the files

        Returns the files of the media library. Use their `url` in image blocks.
        `width` and `height` are `None` for files that are not images.

        :param filter: dict Optional. `name` (part of the file name) and `type`
            (see `FileType`)
        :param sort: str Optional. See `FileSort`. The default is `-created_at`.
        :param page: int Optional. Page number
        :param limit: int Optional. Number of files on a page, from 1 to 100
        :raises: :class: `TypeError` : `filter` type is not valid
        :raises: :class: `ApiError` : API request failed, e.g. the type is not valid
        :return: JSON object
        :rtype: ApiResponse
        """

        query_params = {
            **_params.filter_params(filter),
            **_params.without_none({"sort": sort, "page": page, "limit": limit}),
        }

        return ApiResponse(
            self.api_client.request("GET", self.base_api_url, query_params)
        )
