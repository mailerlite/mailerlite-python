from __future__ import absolute_import

import json
import requests
from urllib.parse import urljoin
from functools import partialmethod
from typing import Optional, Tuple


class HttpMethods(object):
    """Allowed Http methods"""

    GET: str = 'get'
    POST: str = 'post'
    PUT: str = 'put'
    DELETE: str = 'delete'

    # Allowed methods
    ALLOWED: Tuple[str, ...] = (GET, POST, PUT, DELETE)

    @classmethod
    def _is_method(cls, method: str, target: str) -> bool:
        """Checking method names equality"""
        return method == target

    is_get: partialmethod = partialmethod(_is_method, target=GET)
    is_post: partialmethod = partialmethod(_is_method, target=POST)
    is_put: partialmethod = partialmethod(_is_method, target=PUT)
    is_delete: partialmethod = partialmethod(_is_method, target=DELETE)


class ApiClient(object):
    # Base URL of the API
    HOST = 'https://connect.mailerlite.com/'

    # Base headers
    DEFAULT_HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'MailerLite-Python-SDK-Client',
    }

    # Base timeout between requests
    DEFAULT_TIMEOUT = 120

    def __init__(self, config=None) -> None:
        self.headers: dict = self.DEFAULT_HEADERS.copy()
        self.api_key: str = ''
        self.api_version: Optional[str] = None
        self.timeout: Optional[int] = None
        if config is None:
            config = {}
        self.set_config(config)

    def set_config(self, config: dict) -> None:
        """API Client Configuration Setter"""

        # Authentication
        self.api_key = config.get('api_key', '')
        self.headers['Authorization'] = f'Bearer {self.api_key}'

        # API version
        self.api_version = config.get('api_version')
        if self.api_version is not None:
            self.headers['X-Version'] = self.api_version

        # Request timeout
        self.timeout = config.get('timeout', self.DEFAULT_TIMEOUT)

    def request(
        self, method: str, path: str, query_params: Optional[dict] = None, body: Optional[dict] = None
    ) -> requests.models.Response:
        """Requests Wrapper"""

        method = method.lower()
        if method not in HttpMethods.ALLOWED:
            raise ValueError('http method must be `POST`, `GET`, `PUT` or `DELETE`.')

        kwargs = {
            'method': method,
            'url': urljoin(self.HOST, path),
            'params': query_params,
            'headers': self.headers,
            'timeout': self.timeout,
        }
        if HttpMethods.is_get(method):
            kwargs.update(allow_redirects=True)
        if HttpMethods.is_post(method) or HttpMethods.is_put(method):
            kwargs.update(data=json.dumps(body))
        return requests.request(**kwargs)
