# coding: utf-8

from __future__ import absolute_import

from mailerlite.api_client import ApiClient
from mailerlite.sdk.automations import Automations
from mailerlite.sdk.batch import Batches

# import all api files into api package
from mailerlite.sdk.campaigns import Campaigns
from mailerlite.sdk.ecommerce_carts import EcommerceCarts
from mailerlite.sdk.ecommerce_cart_items import EcommerceCartItems
from mailerlite.sdk.ecommerce_categories import EcommerceCategories
from mailerlite.sdk.ecommerce_customers import EcommerceCustomers
from mailerlite.sdk.ecommerce_imports import EcommerceImports
from mailerlite.sdk.ecommerce_orders import EcommerceOrders
from mailerlite.sdk.ecommerce_product_variants import EcommerceProductVariants
from mailerlite.sdk.ecommerce_products import EcommerceProducts
from mailerlite.sdk.ecommerce_settings import EcommerceSettings
from mailerlite.sdk.ecommerce_shops import EcommerceShops
from mailerlite.sdk.fields import Fields
from mailerlite.sdk.forms import Forms
from mailerlite.sdk.groups import Groups
from mailerlite.sdk.segments import Segments
from mailerlite.sdk.subscribers import Subscribers
from mailerlite.sdk.timezones import Timezones
from mailerlite.sdk.webhooks import Webhooks


class Client(object):
    def __init__(self, config={}):
        # Initialize ApiClient
        self.api_client = ApiClient(config)

        # Bootstrap API classes
        self.subscribers = Subscribers(self.api_client)
        self.groups = Groups(self.api_client)
        self.segments = Segments(self.api_client)
        self.fields = Fields(self.api_client)
        self.forms = Forms(self.api_client)
        self.campaigns = Campaigns(self.api_client)
        self.timezones = Timezones(self.api_client)
        self.webhooks = Webhooks(self.api_client)
        self.automations = Automations(self.api_client)
        self.batches = Batches(self.api_client)
        self.ecommerce_shops = EcommerceShops(self.api_client)
        self.ecommerce_products = EcommerceProducts(self.api_client)
        self.ecommerce_product_variants = EcommerceProductVariants(self.api_client)
        self.ecommerce_categories = EcommerceCategories(self.api_client)
        self.ecommerce_customers = EcommerceCustomers(self.api_client)
        self.ecommerce_orders = EcommerceOrders(self.api_client)
        self.ecommerce_carts = EcommerceCarts(self.api_client)
        self.ecommerce_cart_items = EcommerceCartItems(self.api_client)
        self.ecommerce_imports = EcommerceImports(self.api_client)
        self.ecommerce_settings = EcommerceSettings(self.api_client)
