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

    def test_filter_params_removes_the_filters_without_a_value(self):
        assert _params.filter_params({"name": "logo", "type": None}) == {
            "filter[name]": "logo"
        }

    def test_filter_params_rejects_a_filter_that_is_not_a_dict(self):
        with pytest.raises(TypeError, match="filter"):
            _params.filter_params("image")

    def test_query_params_flatten_filter_and_encode_values(self):
        params = _params.query_params(
            {
                "filter": {"status": "active", "id": [1, 2, 3], "enabled": True},
                "with_steps": False,
                "limit": 10,
                "cursor": None,
            },
            ["filter", "with_steps", "limit", "cursor"],
        )

        assert params == {
            "filter[status]": "active",
            "filter[id]": "1,2,3",
            "filter[enabled]": 1,
            "with_steps": 0,
            "limit": 10,
        }

    def test_query_params_drop_none_filter_values(self):
        assert _params.query_params({"filter": {"search": None}}, ["filter"]) == {}

    def test_query_params_reject_unknown_argument(self):
        with pytest.raises(TypeError, match="unknown"):
            _params.query_params({"unknown": 1}, ["filter"])

    def test_query_params_reject_a_filter_that_is_not_a_dict(self):
        with pytest.raises(TypeError, match="filter"):
            _params.query_params({"filter": "active"}, ["filter"])

    def test_body_params_keep_json_types(self):
        body = _params.body_params(
            {"resubscribe": True, "groups": [1, 2]}, ["resubscribe", "groups"]
        )

        assert body == {"resubscribe": True, "groups": [1, 2]}

    def test_body_params_drop_none_and_return_a_new_dict(self):
        kwargs = {"resubscribe": True, "parent_id": None}

        body = _params.body_params(kwargs, ["resubscribe", "parent_id"])

        assert body == {"resubscribe": True}
        assert body is not kwargs
        assert kwargs == {"resubscribe": True, "parent_id": None}

    def test_body_params_reject_unknown_argument(self):
        with pytest.raises(TypeError, match="unknown"):
            _params.body_params({"unknown": 1}, ["resubscribe"])

    def test_idempotency_headers(self):
        assert _params.idempotency_headers(None) is None
        assert _params.idempotency_headers("k1") == {"Idempotency-Key": "k1"}

    @pytest.mark.parametrize(
        "key", ["", " k1", pytest.param("k" * 256, id="256-characters")]
    )
    def test_idempotency_headers_send_the_key_as_given(self, key):
        assert _params.idempotency_headers(key) == {"Idempotency-Key": key}
