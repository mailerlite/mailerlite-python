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

    def test_id_only_methods(self):
        cases = (
            ("delete", "DELETE", "", True),
            ("forget", "POST", "/forget", True),
            ("activity_log", "GET", "/activity-log", False),
            ("assign_subscriber_to_group", "POST", "/groups/42", False),
            ("unassign_subscriber_from_group", "DELETE", "/groups/42", True),
            ("get_import", "GET", None, False),
        )
        for method, verb, suffix, boolean in cases:
            for value in ("31986843064993537", 31986843064993537):
                with self.subTest(method=method, value=value):
                    api = Mock()
                    args = (value, "42") if "group" in method else (value,)
                    result = getattr(Subscribers(api), method)(*args)
                    path = (
                        f"api/subscribers/import/{value}"
                        if suffix is None
                        else f"api/subscribers/{value}{suffix}"
                    )
                    extra = ({},) if method == "activity_log" else ()
                    api.request.assert_called_once_with(verb, path, *extra)
                    self.assertIs(
                        result,
                        True if boolean else api.request.return_value.json.return_value,
                    )

    def test_id_only_methods_reject_invalid_ids(self):
        from mailerlite.exceptions import EmptyIdError, InvalidIdError

        for method in (
            "delete",
            "forget",
            "activity_log",
            "get_import",
            "assign_subscriber_to_group",
            "unassign_subscriber_from_group",
        ):
            for value in (
                True,
                False,
                None,
                1.5,
                "",
                "abc",
                "123\n",
                "１２３",
                "user@example.com",
                "12/34",
            ):
                for position in range(2) if "group" in method else range(1):
                    with self.subTest(method=method, value=value, position=position):
                        api = Mock()
                        args = ["42", "42"] if "group" in method else ["42"]
                        args[position] = value
                        with self.assertRaises(
                            (TypeError, EmptyIdError, InvalidIdError)
                        ):
                            getattr(Subscribers(api), method)(*args)
                        api.request.assert_not_called()

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
                True,
                False,
                None,
                1.5,
                "",
                "abc",
                "12a",
                " 123",
                "123 ",
                "+123",
                "-123",
                "1.2",
                "１２３",
                "١٢٣",
                "²",
                b"123",
            ):
                with self.subTest(method=method, value=value):
                    api = Mock()
                    with self.assertRaises(TypeError):
                        getattr(Subscribers(api), method)(value)
                    api.request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
