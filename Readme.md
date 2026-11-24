<a href="https://www.mailerlite.com"><img src="https://app.mailerlite.com/assets/images/logo-color.png" width="200px"/></a>

# MailerLite Python SDK
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

## Getting started
For more information about MailerLite API, please visit the [following link:](https://developers.mailerlite.com/docs/#mailerlite-api)
### Authentication
API keys are a quick way to implement machine-to-machine authentication without any direct inputs from a human beyond initial setup.

For more information how to obtain an API key visit the [following link](https://developers.mailerlite.com/docs/#mailerlite-api)

## Table of Contents
- [MailerLite Python SDK](#mailerlite-python-sdk)
  - [Getting started](#getting-started)
    - [Authentication](#authentication)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [MailerLite Client](#mailerlite-client)
    - [Error handling](#error-handling)
  - [Subscribers](#subscribers)
    - [List all subscribers](#list-all-subscribers)
    - [Create a subscriber](#create-a-subscriber)
    - [Update a subscriber](#update-a-subscriber)
    - [Get a subscriber](#get-a-subscriber)
    - [Delete a subscriber](#delete-a-subscriber)
    - [Forget a subscriber](#forget-a-subscriber)
    - [Get subscriber activity](#get-subscriber-activity)
  - [Groups](#groups)
    - [List all groups](#list-all-groups)
    - [Create a group](#create-a-group)
    - [Update a group](#update-a-group)
    - [Delete a group](#delete-a-group)
    - [Get subscribers belonging to a group](#get-subscribers-belonging-to-a-group)
    - [Import bulk subscribers to a group](#import-bulk-subscribers-to-a-group)
    - [Assign subscriber to a group](#assign-subscriber-to-a-group)
    - [Unassign subscriber from a group](#unassign-subscriber-from-a-group)
  - [Segments](#segments)
    - [List all segments](#list-all-segments)
    - [Update a segment](#update-a-segment)
    - [Delete a segment](#delete-a-segment)
    - [Get segment information](#get-segment-information)
    - [Get subscribers belonging to a segment](#get-subscribers-belonging-to-a-segment)
  - [Fields](#fields)
    - [List all fields](#list-all-fields)
    - [Create a field](#create-a-field)
    - [Update a field](#update-a-field)
    - [Delete a field](#delete-a-field)
  - [Automations](#automations)
    - [List all automations](#list-all-automations)
    - [Get an automation](#get-an-automation)
    - [Get subscribers activity for an automation](#get-subscribers-activity-for-an-automation)
    - [Create an automation](#create-an-automation)
    - [Update an automation](#update-an-automation)
    - [Delete an automation](#delete-an-automation)
    - [Copy an automation](#copy-an-automation)
    - [Enable an automation](#enable-an-automation)
    - [Disable an automation](#disable-an-automation)
    - [Send a test of an automation](#send-a-test-of-an-automation)
    - [Add subscribers to an automation](#add-subscribers-to-an-automation)
    - [Re-add subscribers to an automation](#re-add-subscribers-to-an-automation)
    - [Copy automation subscribers to groups](#copy-automation-subscribers-to-groups)
    - [Cancel active automation runs](#cancel-active-automation-runs)
    - [Skip an automation delay](#skip-an-automation-delay)
    - [List automation triggers](#list-automation-triggers)
    - [Create an automation trigger](#create-an-automation-trigger)
    - [Get an automation trigger](#get-an-automation-trigger)
    - [Update an automation trigger](#update-an-automation-trigger)
    - [Delete an automation trigger](#delete-an-automation-trigger)
    - [List automation steps](#list-automation-steps)
    - [Create an automation step](#create-an-automation-step)
    - [Get an automation step](#get-an-automation-step)
    - [Update an automation step](#update-an-automation-step)
    - [Delete an automation step](#delete-an-automation-step)
    - [Copy an automation step](#copy-an-automation-step)
    - [Move an automation step](#move-an-automation-step)
    - [Select the winner of an A/B test step](#select-the-winner-of-an-ab-test-step)
    - [Get the content of an automation email](#get-the-content-of-an-automation-email)
    - [Update the content of an automation email](#update-the-content-of-an-automation-email)
    - [Get the report stats of an automation email](#get-the-report-stats-of-an-automation-email)
    - [Get the unsubscribe reasons of an automation email](#get-the-unsubscribe-reasons-of-an-automation-email)
    - [List automation templates](#list-automation-templates)
    - [Create an automation from a template](#create-an-automation-from-a-template)
    - [Get the run counts of automation steps](#get-the-run-counts-of-automation-steps)
    - [Get the run counts of automation triggers](#get-the-run-counts-of-automation-triggers)
    - [Get the stats of A/B test steps](#get-the-stats-of-ab-test-steps)
    - [List the subscribers on an automation step](#list-the-subscribers-on-an-automation-step)
    - [List the subscribers on an automation trigger](#list-the-subscribers-on-an-automation-trigger)
    - [Get the monthly email totals of an automation](#get-the-monthly-email-totals-of-an-automation)
  - [Campaigns](#campaigns)
    - [List all campaigns](#list-all-campaigns)
    - [Get a campaign](#get-a-campaign)
    - [Create a campaign](#create-a-campaign)
    - [Create a simple editor campaign](#create-a-simple-editor-campaign)
    - [Update a campaign](#update-a-campaign)
    - [Schedule a campaign](#schedule-a-campaign)
    - [Cancel a campaign](#cancel-a-campaign)
    - [Delete a campaign](#delete-a-campaign)
    - [Get subscribers activity for a campaign](#get-subscribers-activity-for-a-campaign)
  - [Emails](#emails)
    - [Get an email](#get-an-email)
    - [Get the HTML of an email](#get-the-html-of-an-email)
    - [Get a block](#get-a-block)
    - [Insert a block](#insert-a-block)
    - [Update a block](#update-a-block)
    - [Delete a block](#delete-a-block)
    - [Move a block](#move-a-block)
    - [Validate a block](#validate-a-block)
    - [Update the design settings](#update-the-design-settings)
    - [Validate the design settings](#validate-the-design-settings)
    - [Save an email as a template](#save-an-email-as-a-template)
    - [List the versions of an email](#list-the-versions-of-an-email)
    - [Save a version of an email](#save-a-version-of-an-email)
    - [Restore a version of an email](#restore-a-version-of-an-email)
    - [Retry a write with an idempotency key](#retry-a-write-with-an-idempotency-key)
  - [Brand styles](#brand-styles)
    - [Get the brand styles](#get-the-brand-styles)
  - [Files](#files)
    - [List all files](#list-all-files)
  - [Forms](#forms)
    - [List all forms](#list-all-forms)
    - [Get a form](#get-a-form)
    - [Update a form](#update-a-form)
    - [Delete a form](#delete-a-form)
    - [Get subscribers who signed up to a specific form](#get-subscribers-who-signed-up-to-a-specific-form)
  - [Batching](#batching)
    - [Create a new batch](#create-a-new-batch)
  - [Webhooks](#webhooks)
    - [List all webhooks](#list-all-webhooks)
    - [Get a webhook](#get-a-webhook)
    - [Create a webhook](#create-a-webhook)
    - [Update a webhook](#update-a-webhook)
    - [Delete a webhook](#delete-a-webhook)
  - [Timezones](#timezones)
    - [Get a list of timezones](#get-a-list-of-timezones)
  - [Campaign languages](#campaign-languages)
    - [Get a list of languages](#get-a-list-of-languages)
  - [E-commerce](#e-commerce)
    - [Shops](#shops)
    - [Products and variants](#products-and-variants)
    - [Categories](#categories)
    - [Customers, orders and carts](#customers-orders-and-carts)
    - [Imports](#imports)
    - [Revenue reports and settings](#revenue-reports-and-settings)

## Installation
<a name="installation"></a>

Please run the following command:
```bash
python -m pip install mailerlite
```

## Usage
<a name="usage"></a>

### MailerLite Client
The first thing that you need to do is to import `mailerlite` into your project and to instantiate the client by passing your API key:
```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})
```

MailerLite API supports [versioning](https://developers.mailerlite.com/docs/#versioning), so you can pass additional argument to specify the API version:
```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key", "api_version": "2038-01-19"})
```

### Error handling

API responses with a 4xx or 5xx status code raise a `mailerlite.ApiError` exception. `ApiError` is a subclass of `requests.HTTPError`, so `except requests.HTTPError` continues to work. The exception has these attributes:

- `status_code`: the HTTP status code.
- `message`: the error message of the API.
- `code`: a machine-readable error code, if the API sends one. For example, `version_conflict`.
- `etag`: the current etag of the email, if the API sends one. The API sends it with `version_conflict`.
- `errors`: the validation errors for each field, if the API sends them.
- `response`: the full `requests.Response`.

The attributes are `None` when the response does not have them.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

try:
    response = client.subscribers.get("some@email.com")
except MailerLite.ApiError as e:
    print(e.status_code)  # e.g. 404
    print(e.message)  # error message from the API
    print(e.errors)  # validation errors, if any
    print(e.response.json())  # full error body from the API
```

Network-level failures (DNS errors, connection resets, timeouts) raise the standard `requests` exceptions such as `requests.ConnectionError` and `requests.Timeout`. Catch `requests.RequestException` to handle both HTTP and network errors with a single handler.

**Note:** the batch endpoint (`client.batch.request()`) returns HTTP 200 even when individual sub-requests fail, so no exception is raised for them — check the per-request status codes in the returned body.

**Upgrading from 0.1.x:** methods that previously returned `False` or a raw status code on failure now raise `requests.HTTPError` instead. In particular, `subscribers.delete()` and `subscribers.forget()` used to return `204`/`200` and now return `True` on success.

## Subscribers
<a name="subscribers"></a>

### List all subscribers
<a name="get-a-list-of-subscribers"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.subscribers.list(limit=10, page=1, filter={"status": "active"})
```

### Create a subscriber
<a name="create-a-subscriber"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.subscribers.create(
    "some@email.com",
    fields={"name": "John", "last_name": "Doe"},
    ip_address="1.2.3.4",
    optin_ip="1.2.3.4",
)
```

### Update a subscriber
<a name="update-a-subscriber"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.subscribers.update(
    "some@email.com",
    fields={"name": "New", "last_name": "Name"},
    ip_address="1.2.3.5",
    optin_ip="1.2.3.5",
)
```

`update` sends `PUT /subscribers/{subscriber}`. The first argument is the email address or the ID of the subscriber. The subscriber must exist, or the API returns 404. `groups` replaces the subscriber's groups: groups you leave out are removed. To create a subscriber, or to add groups without removing others, use `create`. Pass `new_email` to change the email address.

### Get a subscriber
<a name="get-a-subscriber"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.subscribers.get("some@email.com")
```

### Delete a subscriber
<a name="delete-a-subscriber"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

subscriber_id = 1234567890

response = client.subscribers.delete(subscriber_id)
```

### Forget a subscriber
<a name="forget-a-subscriber"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

subscriber_id = 1234567890

response = client.subscribers.forget(subscriber_id)
```

### Get subscriber activity
<a name="get-subscriber-activity"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

subscriber_id = 1234567890

response = client.subscribers.activity_log(
    subscriber_id, limit=10, page=1, filter={"log_name": "email_open"}
)
```

## Groups
<a name="groups"></a>

### List all groups
<a name="list-all-groups"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.groups.list(limit=10, page=1, filter={"name": "My"}, sort="name")
```

### Create a group
<a name="create-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

group_name = "My Group"

response = client.groups.create(group_name)
```

### Update a group
<a name="update-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

group_id = 1234567
group_name = "My New Group"

response = client.groups.update(group_id, group_name)
```

### Delete a group
<a name="delete-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

group_id = 1234567

response = client.groups.delete(group_id)
```

### Get subscribers belonging to a group
<a name="get-subscribers-belonging-to-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

group_id = 1234567

response = client.groups.get_group_subscribers(
    group_id, limit=10, filter={"status": "active"}
)

next_cursor = response["meta"]["next_cursor"]
response = client.groups.get_group_subscribers(
    group_id, cursor=next_cursor, limit=10, filter={"status": "active"}
)
```

### Import bulk subscribers to a group
<a name="import-bulk-subscribers-to-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

group_id = 1234567
subscribers = [
    {"email": "subscriber1@example.com", "name": "Subscriber One"},
    {"email": "subscriber2@example.com", "name": "Subscriber Two"},
]

response = client.groups.import_subscribers_to_group(group_id, subscribers)
```

### Assign subscriber to a group
<a name="assign-subscribers-to-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

subscriber_id = 111222
group_id = 1234567

response = client.subscribers.assign_subscriber_to_group(subscriber_id, group_id)
```

### Unassign subscriber from a group
<a name="unassign-subscribers-from-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

subscriber_id = 111222
group_id = 1234567

response = client.subscribers.unassign_subscriber_from_group(subscriber_id, group_id)
```

## Segments
<a name="segments"></a>

### List all segments
<a name="list-all-segments"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.segments.list(limit=10, page=1)
```

### Update a segment
<a name="update-a-segment"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

segment_id = 123456
name = "My New Segment Name"

response = client.segments.update(segment_id, name)
```

### Delete a segment
<a name="delete-a-segment"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

segment_id = 123456

response = client.segments.delete(segment_id)
```

### Get segment information
<a name="get-segment-information"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

segment_id = 123456

response = client.segments.get(segment_id, limit=10, filter={"status": "active"})
```

### Get subscribers belonging to a segment
<a name="get-subscribers-belonging-to-a-segment"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

segment_id = 123456

response = client.segments.get_subscribers(
    segment_id, limit=10, filter={"status": "active"}
)

next_cursor = response["meta"]["next_cursor"]
response = client.segments.get_subscribers(
    segment_id, cursor=next_cursor, limit=10, filter={"status": "active"}
)
```

## Fields
<a name="fields"></a>

### List all fields
<a name="list-all-fields"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.fields.list(
    limit=10, page=1, sort="name", filter={"keyword": "abc", "type": "text"}
)
```

### Create a field
<a name="create-a-field"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

name = "My Field"
type = "text"

response = client.fields.create(name, type)
```

### Update a field
<a name="update-a-field"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

field_id = 123456
name = "My New Field"

response = client.fields.update(field_id, name)
```

### Delete a field
<a name="delete-a-field"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

field_id = 123456

response = client.fields.delete(field_id)
```

## Automations
<a name="automations"></a>

### List all automations
<a name="list-all-automations"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.automations.list(
    limit=10, page=1, filter={"enabled": True, "name": "some name", "group": 123456}
)
```

### Get an automation
<a name="get-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.get(automation_id)
```

### Get subscribers activity for an automation
<a name="get-subscribers-activity-for-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.activity(
    automation_id,
    page=1,
    limit=10,
    filter={"status": "active", "date_from": "2022-12-20", "date_to": "2022-12-31"},
)
```

### Create an automation
<a name="create-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.automations.create("My automation")
```

### Update an automation
<a name="update-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.update(automation_id, "My new name")
```

### Delete an automation
<a name="delete-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.delete(automation_id)
```

### Copy an automation
<a name="copy-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.copy(automation_id)
```

### Enable an automation
<a name="enable-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.enable(automation_id)
```

### Disable an automation
<a name="disable-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.disable(automation_id)
```

### Send a test of an automation
<a name="send-a-test-of-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.test(automation_id, "some@email.com")
```

### Add subscribers to an automation
<a name="add-subscribers-to-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.add_subscribers(
    automation_id, emails=["some@email.com"], groups=[1234567]
)
```

### Re-add subscribers to an automation
<a name="re-add-subscribers-to-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.readd(
    automation_id, "last_completed_step", {"status": "completed"}
)
```

### Copy automation subscribers to groups
<a name="copy-automation-subscribers-to-groups"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.activity_add_to_group(
    automation_id, ["1234567"], {"status": "completed"}
)
```

### Cancel active automation runs
<a name="cancel-active-automation-runs"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.activity_cancel_automation(
    automation_id, {"status": "active"}
)
```

### Skip an automation delay
<a name="skip-an-automation-delay"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.activity_skip_delay(automation_id, {"status": "active"})
```

### List automation triggers
<a name="list-automation-triggers"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.list_triggers(automation_id)
```

### Create an automation trigger
<a name="create-an-automation-trigger"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.create_trigger(
    automation_id, "subscriber_joins_group", data={"group_ids": [1234567]}
)
```

### Get an automation trigger
<a name="get-an-automation-trigger"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
trigger_id = 123456

response = client.automations.get_trigger(automation_id, trigger_id)
```

### Update an automation trigger
<a name="update-an-automation-trigger"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
trigger_id = 123456

response = client.automations.update_trigger(
    automation_id, trigger_id, data={"group_ids": [1234567]}
)
```

### Delete an automation trigger
<a name="delete-an-automation-trigger"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
trigger_id = 123456

response = client.automations.delete_trigger(automation_id, trigger_id)
```

### List automation steps
<a name="list-automation-steps"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.list_steps(automation_id)
```

### Create an automation step
<a name="create-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.create_step(
    automation_id, "delay", parent_id=123456, data={"unit": "days", "value": 1}
)
```

### Get an automation step
<a name="get-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
step_id = 123456

response = client.automations.get_step(automation_id, step_id)
```

### Update an automation step
<a name="update-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
step_id = 123456

response = client.automations.update_step(
    automation_id, step_id, data={"unit": "days", "value": 2}
)
```

### Delete an automation step
<a name="delete-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
step_id = 123456

response = client.automations.delete_step(
    automation_id, step_id, branch_to_delete="all"
)
```

### Copy an automation step
<a name="copy-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
step_id = 123456

response = client.automations.copy_step(automation_id, step_id, parent_id=123456)
```

### Move an automation step
<a name="move-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
step_id = 123456

response = client.automations.reorder_steps(
    automation_id, step_id, new_parent_step_id=123456
)
```

### Select the winner of an A/B test step
<a name="select-the-winner-of-an-ab-test-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
step_id = 123456

response = client.automations.select_ab_test_winner(automation_id, step_id, "a_path")
```

### Get the content of an automation email
<a name="get-the-content-of-an-automation-email"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
email_id = 123456

response = client.automations.get_email_content(automation_id, email_id)
```

### Update the content of an automation email
<a name="update-the-content-of-an-automation-email"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
email_id = 123456

response = client.automations.update_email_content(
    automation_id, email_id, "<p>Hello</p>"
)
```

### Get the report stats of an automation email
<a name="get-the-report-stats-of-an-automation-email"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
email_id = 123456

response = client.automations.email_report_stats(
    automation_id, email_id, start_date="2026-01-01", end_date="2026-01-31"
)
```

### Get the unsubscribe reasons of an automation email
<a name="get-the-unsubscribe-reasons-of-an-automation-email"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
email_id = 123456

response = client.automations.email_unsubscribe_reasons(automation_id, email_id)
```

### List automation templates
<a name="list-automation-templates"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.automations.list_templates(limit=10, page=1, filter={"category": 1})
```

### Create an automation from a template
<a name="create-an-automation-from-a-template"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

template_id = 123456

response = client.automations.select_template(template_id)
```

### Get the run counts of automation steps
<a name="get-the-run-counts-of-automation-steps"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
step_id = 123456

response = client.automations.steps_run_counts(automation_id)
response = client.automations.step_run_counts(automation_id, step_id)
```

### Get the run counts of automation triggers
<a name="get-the-run-counts-of-automation-triggers"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
trigger_id = 123456

response = client.automations.triggers_run_counts(automation_id)
response = client.automations.trigger_run_counts(automation_id, trigger_id)
```

### Get the stats of A/B test steps
<a name="get-the-stats-of-ab-test-steps"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
step_id = 123456

response = client.automations.ab_steps_stats(automation_id)
response = client.automations.ab_step_stats(automation_id, step_id)
```

### List the subscribers on an automation step
<a name="list-the-subscribers-on-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
step_id = 123456

response = client.automations.step_subscribers(
    automation_id, step_id, "queued", limit=10, page=1
)
```

### List the subscribers on an automation trigger
<a name="list-the-subscribers-on-an-automation-trigger"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456
trigger_id = 123456

response = client.automations.trigger_subscribers(
    automation_id, trigger_id, "completed", limit=10, page=1
)
```

### Get the monthly email totals of an automation
<a name="get-the-monthly-email-totals-of-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

automation_id = 123456

response = client.automations.email_monthly_totals(
    automation_id, start_date="2026-01-01", end_date="2026-06-30"
)
```

## Campaigns
<a name="campaigns"></a>

### List all campaigns
<a name="list-all-campaigns"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.campaigns.list(
    limit=10, page=1, filter={"status": "ready", "type": "regular"}
)
```

### Get a campaign
<a name="get-a-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

campaign_id = 123456

response = client.campaigns.get(campaign_id)
```

### Create a campaign
<a name="create-a-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

params = {
    "name": "Test Campaign",
    "language_id": 1,
    "type": "regular",
    "emails": [
        {
            "subject": "This is a test campaign",
            "from_name": "Test Man",
            "from": "testuser@mailerlite.com",
            "content": "Hi there, this is a test campaign!",
        }
    ],
}

response = client.campaigns.create(params)
```

### Create a simple editor campaign
<a name="create-a-simple-editor-campaign"></a>

To build the email with the simple editor, set `editor` to `MailerLite.EDITOR_SIMPLE`, and do not send `content`. Then edit the email with [the email methods](#emails).

- `template_id` is optional. It is the simple editor template that the email starts from: a template from the shared gallery, or a template that you saved from your own email with [`create_template`](#save-an-email-as-a-template). It needs `editor`.
- All emails of a campaign must have the same `editor` and `template_id`.
- Only `create` accepts `editor` and `template_id`. `update` does not.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

params = {
    "name": "Test Campaign",
    "type": "regular",
    "emails": [
        {
            "subject": "This is a test campaign",
            "from_name": "Test Man",
            "from": "testuser@mailerlite.com",
            "editor": MailerLite.EDITOR_SIMPLE,
        }
    ],
}

response = client.campaigns.create(params)

email_id = response["data"]["emails"][0]["id"]
```

### Update a campaign
<a name="update-a-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

campaign_id = 123456
params = {
    "name": "New Campaign Name",
    "language_id": 2,
    "emails": [
        {
            "subject": "This is a test campaign",
            "from_name": "Test Man",
            "from": "testuser@mailerlite.com",
            "content": "Hi there, this is a test campaign!",
        }
    ],
}

response = client.campaigns.update(campaign_id, params)
```

### Schedule a campaign
<a name="schedule-a-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

campaign_id = 123456
params = {
    "delivery": "scheduled",
    "schedule": {"date": "2022-12-31", "hours": "22", "minutes": "00"},
}

response = client.campaigns.schedule(campaign_id, params)
```

### Cancel a campaign
<a name="cancel-a-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

campaign_id = 123456

response = client.campaigns.cancel(campaign_id)
```

### Delete a campaign
<a name="cancel-a-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

campaign_id = 123456

response = client.campaigns.delete(campaign_id)
```

### Get subscribers activity for a campaign
<a name="get-subscribers-activity-for-an-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

campaign_id = 123456

response = client.campaigns.activity(campaign_id)
```

## Emails
<a name="emails"></a>

These methods edit emails built with the simple editor. To create such an email, [create a simple editor campaign](#create-a-simple-editor-campaign). The ID of the email is in `response['data']['emails'][0]['id']`.

- IDs are strings of digits. You can also give them as `int`. An empty ID raises `mailerlite.EmptyIdError`, and an ID that does not contain only digits raises `mailerlite.InvalidIdError`. The SDK sends no request in these cases.
- Before the request, the SDK checks only the IDs and the `settings` of `update_settings()`. It sends all other values as you give them, and the API checks them. An invalid value raises `mailerlite.ApiError`, for example with status `422`.
- The methods return a `mailerlite.ApiResponse`. It is a `dict` with the response body, and it also has `status_code` and `headers`.
- Each write needs the etag from the last response for the email, and returns a new etag. The etag covers the whole email, so send the writes to one email one after another.
- If the email changed after you read it, the write raises `mailerlite.ApiError` with `code` equal to `mailerlite.VERSION_CONFLICT`. Its `etag` is the current etag. Get the email again, and then repeat the write with the current etag.
- The keys of `editor_content` are camelCase, for example `textAlign`. The SDK sends them as you give them.

### Get an email
<a name="get-an-email"></a>

Returns the email with its settings and blocks, and the etag of the email.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"

response = client.emails.get(email_id)

email = response["data"]
etag = response["etag"]
```

### Get the HTML of an email
<a name="get-the-html-of-an-email"></a>

Returns the HTML that the email sends. The API can return a temporary `503` error. If it does, try again later.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"

response = client.emails.get_html(email_id)

html = response["data"]["html"]
```

### Get a block
<a name="get-a-block"></a>

Returns the block and its place in the email: `placement` has the IDs of the blocks `after` and `before` it, or `None`.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"
block_id = "57"

response = client.emails.get_block(email_id, block_id)

block = response["data"]
```

### Insert a block
<a name="insert-a-block"></a>

Use the block types in `MailerLite.BlockType`. `editor_content` can be empty. Without `placement`, the API puts the block at the end of the email. The `before` and `after` positions also need a `block_id`. The API ignores the `block_id` of `start` and `end`. The SDK sends the placement as you give it.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"
etag = client.emails.get(email_id)["etag"]

response = client.emails.create_block(
    email_id,
    etag,
    MailerLite.BlockType.PARAGRAPH,
    {"attrs": {"textAlign": "left"}, "content": [{"type": "text", "text": "Hello"}]},
    placement={"position": MailerLite.BlockPosition.START},
)

block_id = response["data"]["id"]
etag = response["etag"]
```

### Update a block
<a name="update-a-block"></a>

The new `editor_content` replaces the whole content of the block. The API removes the keys that you do not send.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"
block_id = "57"
etag = "etag-from-the-last-response"

response = client.emails.update_block(
    email_id,
    block_id,
    etag,
    {
        "attrs": {"textAlign": "center"},
        "content": [{"type": "text", "text": "Hello again"}],
    },
)

etag = response["etag"]
```

### Delete a block
<a name="delete-a-block"></a>

Also deletes the blocks in it. The response has only the new etag.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"
block_id = "57"
etag = "etag-from-the-last-response"

response = client.emails.delete_block(email_id, block_id, etag)

etag = response["etag"]
```

### Move a block
<a name="move-a-block"></a>

The `before` and `after` positions also need a `block_id`. The API ignores the `block_id` of `start` and `end`. The SDK sends the placement as you give it.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"
block_id = "57"
etag = "etag-from-the-last-response"

response = client.emails.move_block(
    email_id,
    block_id,
    etag,
    {"position": MailerLite.BlockPosition.AFTER, "block_id": "12"},
)

etag = response["etag"]
```

### Validate a block
<a name="validate-a-block"></a>

Checks a block before you insert it. It needs no email and no etag. An invalid block does not raise an error: the response has `valid` set to `False` and the `errors` for each field.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.emails.validate_block(
    MailerLite.BlockType.BUTTON,
    {
        "attrs": {"href": "https://example.com"},
        "content": [{"type": "text", "text": "Buy now"}],
    },
)

if not response["valid"]:
    print(response["errors"])
```

### Update the design settings
<a name="update-the-design-settings"></a>

Send only the keys to change, in the shape of `settings` in the email. The groups are `brand`, `layout`, `typography`, `button` and `footer`.

- Send all style values as strings, for example `'16'` and not `16`.
- The API stores each value that you send, also a value that the email inherits from your account. Then the email no longer follows your account for that value.
- To unset a brand colour, send an empty string. The API stores the value empty, and the email then uses the account value.
- To unset a footer text, send an empty editor document: `{'editor_content': {}}` or `{'editor_content': {'content': []}}`.
- Other colours, sizes, `button.border_radius` and `brand.style` cannot be empty. An empty string gives a `422` error.
- `footer.social_links` replaces the whole list. Keep the `link_id` of each link to keep its click history.
- `brand.mode` is one of `MailerLite.BrandMode`. To apply a preset palette, send its `identifier` from [the brand styles](#get-the-brand-styles) in `brand.style`.
- If the API removed unsafe values, the response has `rejected` with the keys of these values.
- `settings` must be a `dict` without an `etag` key, because the SDK adds the `etag` argument to it. Otherwise the SDK raises `TypeError` or `ValueError` and sends no request.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"
etag = "etag-from-the-last-response"

response = client.emails.update_settings(
    email_id,
    etag,
    {
        "brand": {"mode": MailerLite.BrandMode.CUSTOM, "background_color": "#f4f4f4"},
        "typography": {"paragraph": {"p1": {"size": "18"}}},
    },
)

etag = response["etag"]
if response.get("rejected"):
    print(response["rejected"]["keys"])
```

### Validate the design settings
<a name="validate-the-design-settings"></a>

Checks a change with the rules of the update, and saves nothing. It needs no etag. Invalid settings do not raise an error: the response has `valid` set to `False` and the `errors` for each field.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"

response = client.emails.validate_settings(
    email_id,
    {
        "button": {"border_radius": "8"},
    },
)

if not response["valid"]:
    print(response["errors"])
```

### Save an email as a template
<a name="save-an-email-as-a-template"></a>

Copies the email to a new template. The API cannot delete templates.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"

response = client.emails.create_template(email_id, "Monthly newsletter")

template_id = response["data"]["id"]
```

### List the versions of an email
<a name="list-the-versions-of-an-email"></a>

A version is a saved copy of the content and the settings of an email. The list starts with the newest version. `current` marks the version that the email has now.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"

response = client.emails.list_versions(email_id, page=1, limit=10)
```

### Save a version of an email
<a name="save-a-version-of-an-email"></a>

Writes through the API do not save versions. If nothing changed after the last version, the API saves no new version and returns the last version. `response.status_code` is `201` for a new version and `200` for the last version.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"

response = client.emails.create_version(email_id)

version_id = response["data"]["id"]
is_new = response.status_code == 201
```

### Restore a version of an email
<a name="restore-a-version-of-an-email"></a>

Puts the email back to the version, and returns the full email with the new etag. Before the restore, the API saves the current state as a version, so you can undo the restore.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"
version_id = "901"
etag = "etag-from-the-last-response"

response = client.emails.restore_version(email_id, version_id, etag)

etag = response["etag"]
```

### Retry a write with an idempotency key
<a name="retry-a-write-with-an-idempotency-key"></a>

If a write fails with a network error, you do not know if the API did the write. Give the write an `idempotency_key`, and retry it with the same key and the same arguments. If the first request succeeded, the API returns the stored response and does not do the write two times. Then `response.is_idempotent_replay` is `True`.

- Use a new key for each write. The API keeps a key for 24 hours.
- The key must be 1 to 255 printable ASCII characters. The SDK sends the key as you give it. The API answers an invalid key with status `400`.
- If `requests` cannot send the key in a header, it raises `requests.exceptions.InvalidHeader`. For example, a key with a space at the start or a new line causes this error.
- The same key with different arguments raises `ApiError` with status `422`. If the first request is still running, the API returns `409` without a `code`.
- These methods accept a key: `create_block`, `update_block`, `delete_block`, `move_block`, `update_settings`, `create_template`, `create_version` and `restore_version`.

```python
import uuid

import requests
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

email_id = "123456"
etag = "etag-from-the-last-response"
key = str(uuid.uuid4())

try:
    response = client.emails.create_block(
        email_id, etag, MailerLite.BlockType.DIVIDER, {}, idempotency_key=key
    )
except (requests.ConnectionError, requests.Timeout):
    # Network error: retry with the same key and the same arguments.
    response = client.emails.create_block(
        email_id, etag, MailerLite.BlockType.DIVIDER, {}, idempotency_key=key
    )

print(response["data"]["id"], response.is_idempotent_replay)
```

## Brand styles
<a name="brand-styles"></a>

### Get the brand styles
<a name="get-the-brand-styles"></a>

Returns the palettes of your account: `brand` (your brand styles, or `None` if your account has none), `default` and the `presets`. Match a palette on its `identifier`, not on its `name`. To apply a preset to an email, [update the design settings](#update-the-design-settings) with `{'brand': {'style': identifier}}`.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.brand_styles.get()

identifiers = [preset["identifier"] for preset in response["data"]["presets"]]
```

## Files
<a name="files"></a>

### List all files
<a name="list-all-files"></a>

Returns the files of your media library. Use their `url` in image blocks. `width` and `height` are `None` for files that are not images.

- `filter`: `name` (a part of the file name) and `type` (one of `MailerLite.FileType`).
- `sort`: one of `MailerLite.FileSort`. The default is newest first.

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.files.list(
    filter={"name": "summer sale", "type": MailerLite.FileType.IMAGE},
    sort=MailerLite.FileSort.SIZE_DESCENDING,
    page=1,
    limit=25,
)
```

## Forms
<a name="forms"></a>

### List all forms
<a name="list-all-forms"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.forms.list(
    limit=10, page=1, sort="name", filter={"name": "form name"}
)
```

### Get a form
<a name="get-a-form"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

form_id = 123456

response = client.forms.get(form_id)
```

### Update a form
<a name="update-a-form"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

form_id = 123456
name = "New Form Name"

response = client.forms.update(form_id, name)
```

### Delete a form
<a name="cancel-a-form"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

form_id = 123456

response = client.forms.delete(form_id)
```

### Get subscribers who signed up to a specific form
<a name="get-subscribers-who-signed-up-to-a-specific-form"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

form_id = 123456

response = client.forms.get_subscribers(
    form_id, page=1, limit=10, filter={"status": "active"}
)
```

## Batching
<a name="batching"></a>

### Create a new batch
<a name="create-a-new-batch"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

params = [
    {"method": "GET", "path": "api/subscribers/list"},
    {"method": "GET", "path": "api/campaigns/list"},
]

response = self.client.batches.request(params)
```

## Webhooks
<a name="webhooks"></a>

### List all webhooks
<a name="list-all-webhooks"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.webhooks.list()
```

### Get a webhook
<a name="get-a-webhook"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

webhook_id = 123456

response = client.webhooks.get(webhook_id)
```

### Create a webhook
<a name="create-a-webhook"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

events = ["subscriber.created", "subscriber.updated", "subscriber.unsubscribed"]
url = "https://my-url.com"
name = "Webhook name"

response = client.webhooks.create(events, url, name)
```

### Update a webhook
<a name="update-a-webhook"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

webhook_id = 123456
events = ["subscriber.created", "subscriber.updated", "subscriber.unsubscribed"]
url = "https://my-url.com"
name = "Webhook name"
enabled = False

response = client.webhooks.update(webhook_id, events, url, name, enabled)
```

### Delete a webhook
<a name="cancel-a-webhook"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

webhook_id = 123456

response = client.webhooks.delete(webhook_id)
```

## Timezones
<a name="timezones"></a>

### Get a list of timezones
<a name="get-a-list-of-timezones"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.timezone.list()
```

## Campaign languages
<a name="languages"></a>

### Get a list of languages
<a name="get-a-list-of-languages"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({"api_key": "your-api-key"})

response = client.campaigns.languages()
```

## E-commerce
<a name="e-commerce"></a>

Every e-commerce call takes the shop ID first. The examples below assume:

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})
```

### Shops
<a name="shops"></a>

```python
client.ecommerce_shops.list(limit=25)
client.ecommerce_shops.get(1234)
client.ecommerce_shops.create('My shop', 'https://shop.example.com', 'EUR')
client.ecommerce_shops.update(1234, name='New name')
client.ecommerce_shops.delete(1234)
```

### Products and variants
<a name="products-and-variants"></a>

```python
client.ecommerce_products.list(1234, filter={'enabled': True}, sort='-created_at')
client.ecommerce_products.get(1234, 5678)
client.ecommerce_products.create(1234, 'Red T-shirt', price=19.99)
client.ecommerce_products.update(1234, 5678, price=24.99)
client.ecommerce_products.delete(1234, 5678)
client.ecommerce_products.change_status(1234, 5678, False)
client.ecommerce_products.assign_categories(1234, 5678, [91], replace=True)

client.ecommerce_product_variants.list(1234, 5678)
client.ecommerce_product_variants.sync(1234, 5678, [{'name': 'Large', 'attributes': {'size': 'L'}, 'resource_id': 'variant-l'}])
client.ecommerce_product_variants.update(1234, 5678, 42, 'Extra large', {'size': 'XL'})
client.ecommerce_product_variants.delete(1234, 5678, 42)
```

### Categories
<a name="categories"></a>

```python
client.ecommerce_categories.list(1234)
client.ecommerce_categories.get(1234, 91)
client.ecommerce_categories.create(1234, 'Hats')
client.ecommerce_categories.update(1234, 91, name='Caps')
client.ecommerce_categories.delete(1234, 91)
client.ecommerce_categories.products(1234, 91)
client.ecommerce_categories.assign_product(1234, 91, 5678)
client.ecommerce_categories.unassign_product(1234, 91, 5678)
```

### Customers, orders and carts
<a name="customers-orders-and-carts"></a>

```python
client.ecommerce_customers.list(1234, filter={'email': 'customer@example.com'})
client.ecommerce_customers.create(1234, 'customer@example.com', create_subscriber=True)
client.ecommerce_customers.update(1234, 77, name='Jane')
client.ecommerce_customers.delete(1234, 77)

client.ecommerce_orders.list(1234, filter={'attributed': True, 'email_id': 555})
client.ecommerce_orders.create(
    1234,
    {'email': 'customer@example.com'},
    {'items': [{'ecommerce_product_id': 5678, 'quantity': 1, 'price': 19.99}]},
    status='complete',
)
client.ecommerce_orders.update(1234, 99, status='complete')
client.ecommerce_orders.delete(1234, 99)

client.ecommerce_carts.list(1234)
client.ecommerce_carts.update(1234, 33, checkout_url='https://shop.example.com/cart')
client.ecommerce_cart_items.list(1234, 33)
client.ecommerce_cart_items.update(1234, 33, 8, quantity=2)
client.ecommerce_cart_items.delete(1234, 33, 8)
```

### Imports
<a name="imports"></a>

```python
client.ecommerce_imports.products(1234, [{'name': 'Red T-shirt', 'price': 19.99}])
client.ecommerce_imports.categories(1234, [{'name': 'Hats'}])
client.ecommerce_imports.customers(1234, [{'email': 'customer@example.com'}])
```

### Revenue reports and settings
<a name="revenue-reports-and-settings"></a>

```python
client.ecommerce_shops.stats(1234, '2026-10-01', '2026-10-31')

client.campaigns.ecommerce_stats(1111, 1234)
client.campaigns.ecommerce_orders(1111, 1234)

client.subscribers.ecommerce_stats(2222, 1234)
client.subscribers.ecommerce_orders(2222, 1234)

client.automations.ecommerce_stats(3333)
client.automations.email_ecommerce_stats(3333, 4444)
client.automations.ecommerce_orders(3333, 'all_time')

client.ecommerce_settings.get()
```
