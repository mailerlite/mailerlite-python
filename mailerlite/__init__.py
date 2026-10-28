# coding: utf-8

from __future__ import absolute_import

from mailerlite.api_client import ApiClient
from mailerlite.exceptions import (  # noqa: F401
    ApiError,
    EmptyEtagError,
    EmptyIdError,
    InvalidIdError,
)
from mailerlite.response import ApiResponse  # noqa: F401
from mailerlite.sdk.automations import Automations
from mailerlite.sdk.batch import Batches
from mailerlite.sdk.brand_styles import BrandStyles

# import all api files into api package
from mailerlite.sdk.campaigns import Campaigns
from mailerlite.sdk.emails import (  # noqa: F401
    EDITOR_SIMPLE,
    VERSION_CONFLICT,
    BlockPosition,
    BlockType,
    BrandMode,
    Emails,
)
from mailerlite.sdk.fields import Fields
from mailerlite.sdk.files import FileSort, Files, FileType  # noqa: F401
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
        self.emails = Emails(self.api_client)
        self.brand_styles = BrandStyles(self.api_client)
        self.files = Files(self.api_client)
        self.timezones = Timezones(self.api_client)
        self.webhooks = Webhooks(self.api_client)
        self.automations = Automations(self.api_client)
        self.batches = Batches(self.api_client)
