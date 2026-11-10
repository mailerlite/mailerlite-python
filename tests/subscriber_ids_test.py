import unittest
from unittest.mock import Mock

from mailerlite.sdk.subscribers import Subscribers


class SubscriberIdsTest(unittest.TestCase):
    def test_get_accepts_numeric_string_id(self):
        api = Mock()
        subscriber_id = "31986843064993537"
        result = Subscribers(api).get(subscriber_id)
        api.request.assert_called_once_with("GET", f"api/subscribers/{subscriber_id}")
        self.assertIs(result, api.request.return_value.json.return_value)

    def test_update_accepts_numeric_string_id(self):
        api = Mock()
        subscriber_id = "31986843064993537"
        result = Subscribers(api).update(subscriber_id, status="active")
        api.request.assert_called_once_with(
            "PUT", f"api/subscribers/{subscriber_id}", body={"status": "active"}
        )
        self.assertIs(result, api.request.return_value.json.return_value)

    def test_existing_identifiers_remain_supported(self):
        for method in ("get", "update"):
            for value in (31986843064993537, "user@example.com"):
                with self.subTest(method=method, value=value):
                    api = Mock()
                    getattr(Subscribers(api), method)(value)
                    api.request.assert_called_once()

    def test_invalid_identifiers_do_not_send_requests(self):
        for method in ("get", "update"):
            for value in (
                True, False, None, 1.5, "", "abc", "12a", " 123", "123 ",
                "+123", "-123", "1.2", "１２３", "١٢٣", "²", b"123",
            ):
                with self.subTest(method=method, value=value):
                    api = Mock()
                    with self.assertRaises(TypeError):
                        getattr(Subscribers(api), method)(value)
                    api.request.assert_not_called()
