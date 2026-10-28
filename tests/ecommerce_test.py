import json

import mailerlite as MailerLite
import pytest

API = "https://connect.mailerlite.com/api"
SHOP = f"{API}/ecommerce/shops/1"
VARIANT = {"name": "Large", "attributes": {"size": "L"}}

REQUESTS = [
    (
        lambda c: c.ecommerce_shops.list(limit=10),
        "get",
        f"{API}/ecommerce/shops",
        {"limit": 10},
        None,
    ),
    (lambda c: c.ecommerce_shops.get(1), "get", SHOP, None, None),
    (
        lambda c: c.ecommerce_shops.create("Shop", "https://shop.test", "EUR"),
        "post",
        f"{API}/ecommerce/shops",
        None,
        {"name": "Shop", "url": "https://shop.test", "currency": "EUR"},
    ),
    (
        lambda c: c.ecommerce_shops.update(1, name="New"),
        "put",
        SHOP,
        None,
        {"name": "New"},
    ),
    (lambda c: c.ecommerce_shops.delete(1), "delete", SHOP, None, None),
    (
        lambda c: c.ecommerce_shops.stats(1, "2026-10-01", "2026-10-31"),
        "get",
        f"{SHOP}/reports/stats",
        {"start_date": "2026-10-01", "end_date": "2026-10-31"},
        None,
    ),
    (
        lambda c: c.ecommerce_settings.get(),
        "get",
        f"{API}/ecommerce/settings",
        None,
        None,
    ),
    (
        lambda c: c.ecommerce_products.list(1, filter={"enabled": True}, sort="-name"),
        "get",
        f"{SHOP}/products",
        {"filter[enabled]": True, "sort": "-name"},
        None,
    ),
    (lambda c: c.ecommerce_products.get(1, 7), "get", f"{SHOP}/products/7", None, None),
    (
        lambda c: c.ecommerce_products.create(1, "Hat", price=19.99),
        "post",
        f"{SHOP}/products",
        None,
        {"name": "Hat", "price": 19.99},
    ),
    (
        lambda c: c.ecommerce_products.update(1, 7, name="Cap"),
        "put",
        f"{SHOP}/products/7",
        None,
        {"name": "Cap"},
    ),
    (
        lambda c: c.ecommerce_products.delete(1, 7),
        "delete",
        f"{SHOP}/products/7",
        None,
        None,
    ),
    (
        lambda c: c.ecommerce_products.change_status(1, 7, False),
        "put",
        f"{SHOP}/products/7/change-status",
        None,
        {"status": False},
    ),
    (
        lambda c: c.ecommerce_products.assign_categories(1, 7, [5], replace=True),
        "put",
        f"{SHOP}/products/7/categories/multiple",
        None,
        {"categories": [5], "replace": True},
    ),
    (
        lambda c: c.ecommerce_product_variants.list(1, 7),
        "get",
        f"{SHOP}/products/7/variants",
        None,
        None,
    ),
    (
        lambda c: c.ecommerce_product_variants.sync(1, 7, [VARIANT]),
        "post",
        f"{SHOP}/products/7/variants",
        None,
        [VARIANT],
    ),
    (
        lambda c: c.ecommerce_product_variants.update(1, 7, 3, "Large", {"size": "L"}),
        "put",
        f"{SHOP}/products/7/variants/3",
        None,
        VARIANT,
    ),
    (
        lambda c: c.ecommerce_product_variants.delete(1, 7, 3),
        "delete",
        f"{SHOP}/products/7/variants/3",
        None,
        None,
    ),
    (lambda c: c.ecommerce_categories.list(1), "get", f"{SHOP}/categories", {}, None),
    (
        lambda c: c.ecommerce_categories.get(1, 5),
        "get",
        f"{SHOP}/categories/5",
        None,
        None,
    ),
    (
        lambda c: c.ecommerce_categories.create(1, "Hats"),
        "post",
        f"{SHOP}/categories",
        None,
        {"name": "Hats"},
    ),
    (
        lambda c: c.ecommerce_categories.update(1, 5, name="Caps"),
        "put",
        f"{SHOP}/categories/5",
        None,
        {"name": "Caps"},
    ),
    (
        lambda c: c.ecommerce_categories.delete(1, 5),
        "delete",
        f"{SHOP}/categories/5",
        None,
        None,
    ),
    (
        lambda c: c.ecommerce_categories.products(1, 5),
        "get",
        f"{SHOP}/categories/5/products",
        {},
        None,
    ),
    (
        lambda c: c.ecommerce_categories.assign_product(1, 5, 7),
        "put",
        f"{SHOP}/categories/5/products/7",
        None,
        {},
    ),
    (
        lambda c: c.ecommerce_categories.unassign_product(1, 5, 7),
        "delete",
        f"{SHOP}/categories/5/products/7",
        None,
        None,
    ),
    (
        lambda c: c.ecommerce_customers.list(1, filter={"email": "a@b.test"}),
        "get",
        f"{SHOP}/customers",
        {"filter[email]": "a@b.test"},
        None,
    ),
    (
        lambda c: c.ecommerce_customers.get(1, 3),
        "get",
        f"{SHOP}/customers/3",
        None,
        None,
    ),
    (
        lambda c: c.ecommerce_customers.create(1, "a@b.test"),
        "post",
        f"{SHOP}/customers",
        None,
        {"email": "a@b.test"},
    ),
    (
        lambda c: c.ecommerce_customers.update(1, 3, name="Jane"),
        "put",
        f"{SHOP}/customers/3",
        None,
        {"name": "Jane"},
    ),
    (
        lambda c: c.ecommerce_customers.delete(1, 3),
        "delete",
        f"{SHOP}/customers/3",
        None,
        None,
    ),
    (
        lambda c: c.ecommerce_orders.list(
            1, filter={"attributed": True, "email_id": 55}
        ),
        "get",
        f"{SHOP}/orders",
        {"filter[attributed]": True, "filter[email_id]": 55},
        None,
    ),
    (lambda c: c.ecommerce_orders.get(1, 9), "get", f"{SHOP}/orders/9", None, None),
    (
        lambda c: c.ecommerce_orders.create(
            1, {"email": "a@b.test"}, {"items": [{"ecommerce_product_id": 7}]}
        ),
        "post",
        f"{SHOP}/orders",
        None,
        {
            "customer": {"email": "a@b.test"},
            "cart": {"items": [{"ecommerce_product_id": 7}]},
        },
    ),
    (
        lambda c: c.ecommerce_orders.update(1, 9, status="complete"),
        "put",
        f"{SHOP}/orders/9",
        None,
        {"status": "complete"},
    ),
    (
        lambda c: c.ecommerce_orders.delete(1, 9),
        "delete",
        f"{SHOP}/orders/9",
        None,
        None,
    ),
    (lambda c: c.ecommerce_carts.list(1), "get", f"{SHOP}/carts", {}, None),
    (lambda c: c.ecommerce_carts.get(1, 4), "get", f"{SHOP}/carts/4", None, None),
    (
        lambda c: c.ecommerce_carts.update(1, 4, cart_total=10),
        "put",
        f"{SHOP}/carts/4",
        None,
        {"cart_total": 10},
    ),
    (
        lambda c: c.ecommerce_cart_items.list(1, 4),
        "get",
        f"{SHOP}/carts/4/items",
        {},
        None,
    ),
    (
        lambda c: c.ecommerce_cart_items.get(1, 4, 8),
        "get",
        f"{SHOP}/carts/4/items/8",
        None,
        None,
    ),
    (
        lambda c: c.ecommerce_cart_items.create(1, 4, ecommerce_product_id=7),
        "post",
        f"{SHOP}/carts/4/items",
        None,
        {"ecommerce_product_id": 7},
    ),
    (
        lambda c: c.ecommerce_cart_items.update(1, 4, 8, quantity=2),
        "put",
        f"{SHOP}/carts/4/items/8",
        None,
        {"quantity": 2},
    ),
    (
        lambda c: c.ecommerce_cart_items.delete(1, 4, 8),
        "delete",
        f"{SHOP}/carts/4/items/8",
        None,
        None,
    ),
    (
        lambda c: c.ecommerce_imports.products(1, [{"name": "Hat"}]),
        "post",
        f"{SHOP}/products/import",
        None,
        [{"name": "Hat"}],
    ),
    (
        lambda c: c.ecommerce_imports.categories(1, [{"name": "Hats"}]),
        "post",
        f"{SHOP}/categories/import",
        None,
        [{"name": "Hats"}],
    ),
    (
        lambda c: c.ecommerce_imports.customers(1, [{"email": "a@b.test"}]),
        "post",
        f"{SHOP}/customers/import",
        None,
        [{"email": "a@b.test"}],
    ),
    (
        lambda c: c.campaigns.ecommerce_stats(2, 1),
        "get",
        f"{API}/campaigns/2/reports/ecommerce",
        {"shop_id": 1},
        None,
    ),
    (
        lambda c: c.campaigns.ecommerce_orders(2, 1, page=2),
        "get",
        f"{API}/campaigns/2/reports/ecommerce/orders",
        {"shop_id": 1, "page": 2},
        None,
    ),
    (
        lambda c: c.subscribers.ecommerce_stats(6, 1),
        "get",
        f"{API}/subscribers/6/reports/ecommerce",
        {"shop_id": 1},
        None,
    ),
    (
        lambda c: c.subscribers.ecommerce_orders(6, 1),
        "get",
        f"{API}/subscribers/6/reports/ecommerce/orders",
        {"shop_id": 1},
        None,
    ),
    (
        lambda c: c.automations.ecommerce_stats(8),
        "get",
        f"{API}/automations/8/monthly-totals/ecommerce",
        {},
        None,
    ),
    (
        lambda c: c.automations.email_ecommerce_stats(8, 9, shop_id=1),
        "get",
        f"{API}/automations/8/emails/9/ecommerce-overview-stats",
        {"shop_id": 1},
        None,
    ),
    (
        lambda c: c.automations.ecommerce_orders(8, "all_time"),
        "get",
        f"{API}/automations/8/order-activity",
        {"time_frame": "all_time"},
        None,
    ),
]


class TestEcommerce:
    @classmethod
    def setup_class(self):
        self.client = MailerLite.Client({"api_key": "test-key"})

    @pytest.mark.parametrize("call, method, url, params, body", REQUESTS)
    def test_request(self, mocker, call, method, url, params, body):
        request = mocker.patch("requests.request")
        request.return_value.json.return_value = {}

        call(self.client)

        kwargs = request.call_args.kwargs
        assert kwargs["method"] == method
        assert kwargs["url"] == url
        assert kwargs["params"] == params
        if body is not None:
            assert json.loads(kwargs["data"]) == body

    def test_rejects_a_non_integer_id(self):
        with pytest.raises(TypeError):
            self.client.ecommerce_products.get(1, "7")

    def test_rejects_an_unknown_list_argument(self):
        with pytest.raises(TypeError):
            self.client.ecommerce_products.list(1, unknown=True)
