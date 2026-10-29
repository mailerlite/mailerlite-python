import pytest
from mailerlite.exceptions import (
    EmptyEtagError,
    EmptyIdError,
    InvalidIdempotencyKeyError,
    InvalidIdError,
)
from mailerlite.sdk import _params


class TestParams:
    def test_path_id_returns_the_id_as_a_string(self):
        assert _params.path_id(123, "email_id") == "123"
        assert _params.path_id("123", "email_id") == "123"

    @pytest.mark.parametrize(
        "value, error",
        [
            ("", EmptyIdError),
            (None, EmptyIdError),
            ("12/3", InvalidIdError),
            (True, TypeError),
            (1.5, TypeError),
        ],
    )
    def test_path_id_rejects_an_invalid_id(self, value, error):
        with pytest.raises(error, match="email_id"):
            _params.path_id(value, "email_id")

    def test_etag_returns_the_etag(self):
        assert _params.etag("42") == "42"

    @pytest.mark.parametrize("value, error", [("", EmptyEtagError), (42, TypeError)])
    def test_etag_rejects_an_invalid_etag(self, value, error):
        with pytest.raises(error):
            _params.etag(value)

    def test_require_dict_rejects_a_value_that_is_not_a_dict(self):
        _params.require_dict({}, "settings")

        with pytest.raises(TypeError, match="settings"):
            _params.require_dict([], "settings")

    def test_without_none_removes_the_keys_without_a_value(self):
        assert _params.without_none({"page": 2, "limit": None}) == {"page": 2}

    def test_idempotency_headers(self):
        assert _params.idempotency_headers(None) is None
        assert _params.idempotency_headers("k1") == {"Idempotency-Key": "k1"}

        with pytest.raises(InvalidIdempotencyKeyError):
            _params.idempotency_headers(" k1")
