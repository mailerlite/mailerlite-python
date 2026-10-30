import pytest
from mailerlite.exceptions import EmptyIdError, InvalidIdError
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

    def test_require_dict_rejects_a_value_that_is_not_a_dict(self):
        _params.require_dict({}, "settings")

        with pytest.raises(TypeError, match="settings"):
            _params.require_dict([], "settings")

    def test_without_none_removes_the_keys_without_a_value(self):
        assert _params.without_none({"page": 2, "limit": None}) == {"page": 2}

    def test_filter_params_returns_a_query_param_for_each_filter(self):
        assert _params.filter_params(None) == {}
        assert _params.filter_params({"name": "logo", "type": "image"}) == {
            "filter[name]": "logo",
            "filter[type]": "image",
        }

    def test_filter_params_rejects_a_filter_that_is_not_a_dict(self):
        with pytest.raises(TypeError, match="filter"):
            _params.filter_params("image")

    def test_idempotency_headers(self):
        assert _params.idempotency_headers(None) is None
        assert _params.idempotency_headers("k1") == {"Idempotency-Key": "k1"}

    @pytest.mark.parametrize(
        "key", ["", " k1", pytest.param("k" * 256, id="256-characters")]
    )
    def test_idempotency_headers_send_the_key_as_given(self, key):
        assert _params.idempotency_headers(key) == {"Idempotency-Key": key}
