import pytest

from mailerlite.sdk._request_params import body_params, query_params


class TestRequestParams:
    def test_query_params_flatten_filter_and_encode_values(self):
        params = query_params(
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
        assert query_params({"filter": {"search": None}}, ["filter"]) == {}

    def test_query_params_reject_unknown_argument(self):
        with pytest.raises(TypeError):
            query_params({"unknown": 1}, ["filter"])

    def test_body_params_keep_json_types(self):
        body = body_params(
            {"resubscribe": True, "groups": [1, 2], "parent_id": None},
            ["resubscribe", "groups", "parent_id"],
        )

        assert body == {"resubscribe": True, "groups": [1, 2], "parent_id": None}

    def test_body_params_reject_unknown_argument(self):
        with pytest.raises(TypeError):
            body_params({"unknown": 1}, ["resubscribe"])
