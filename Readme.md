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
    - [Update a campaign](#update-a-campaign)
    - [Schedule a campaign](#schedule-a-campaign)
    - [Cancel a campaign](#cancel-a-campaign)
    - [Delete a campaign](#delete-a-campaign)
    - [Get subscribers activity for a campaign](#get-subscribers-activity-for-a-campaign)
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

client = MailerLite.Client({
  'api_key': 'your-api-key'
})
```

MailerLite API supports [versioning](https://developers.mailerlite.com/docs/#versioning), so you can pass additional argument to specify the API version:
```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key',
  'api_version': '2038-01-19'
})
```

### Error handling

API responses with a 4xx or 5xx status code raise a `requests.HTTPError` exception. The exception includes the full response, so you can inspect the status code and error body:

```python
import requests
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

try:
    response = client.subscribers.get('some@email.com')
except requests.HTTPError as e:
    print(e.response.status_code)  # e.g. 404
    print(e.response.json())       # error body from the API
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

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.subscribers.list(limit=10, page=1, filter={'status': 'active'})
```

### Create a subscriber
<a name="create-a-subscriber"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.subscribers.create('some@email.com', fields={'name': 'John', 'last_name': 'Doe'}, ip_address='1.2.3.4', optin_ip='1.2.3.4')
```

### Update a subscriber
<a name="update-a-subscriber"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.subscribers.update('some@email.com', fields={'name': 'New', 'last_name': 'Name'}, ip_address='1.2.3.5', optin_ip='1.2.3.5')
```

`update` sends `PUT /subscribers/{subscriber}`. The first argument is the email address or the ID of the subscriber. The subscriber must exist, or the API returns 404. `groups` replaces the subscriber's groups: groups you leave out are removed. To create a subscriber, or to add groups without removing others, use `create`. Pass `new_email` to change the email address.

### Get a subscriber
<a name="get-a-subscriber"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.subscribers.get('some@email.com')
```

### Delete a subscriber
<a name="delete-a-subscriber"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

subscriber_id = 1234567890

response = client.subscribers.delete(subscriber_id)
```

### Forget a subscriber
<a name="forget-a-subscriber"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

subscriber_id = 1234567890

response = client.subscribers.forget(subscriber_id)
```

### Get subscriber activity
<a name="get-subscriber-activity"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

subscriber_id = 1234567890

response = client.subscribers.activity_log(subscriber_id, limit=10, page=1, filter={'log_name': 'email_open'})
```

## Groups
<a name="groups"></a>

### List all groups
<a name="list-all-groups"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.groups.list(limit=10, page=1, filter={'name': 'My'}, sort='name')
```

### Create a group
<a name="create-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

group_name = 'My Group'

response = client.groups.create(group_name)
```

### Update a group
<a name="update-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

group_id = 1234567
group_name = 'My New Group'

response = client.groups.update(group_id, group_name)
```

### Delete a group
<a name="delete-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

group_id = 1234567

response = client.groups.delete(group_id)
```

### Get subscribers belonging to a group
<a name="get-subscribers-belonging-to-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

group_id = 1234567

response = client.groups.get_group_subscribers(group_id, limit=10, filter={'status': 'active'})

next_cursor = response['meta']['next_cursor']
response = client.groups.get_group_subscribers(group_id, cursor=next_cursor, limit=10, filter={'status': 'active'})
```

### Import bulk subscribers to a group
<a name="import-bulk-subscribers-to-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

group_id = 1234567
subscribers = [
    {'email': 'subscriber1@example.com', 'name': 'Subscriber One'},
    {'email': 'subscriber2@example.com', 'name': 'Subscriber Two'},
]

response = client.groups.import_subscribers_to_group(group_id, subscribers)
```

### Assign subscriber to a group
<a name="assign-subscribers-to-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

subscriber_id = 111222
group_id = 1234567

response = client.subscribers.assign_subscriber_to_group(subscriber_id, group_id)
```

### Unassign subscriber from a group
<a name="unassign-subscribers-from-a-group"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

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

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.segments.list(limit=10, page=1)
```

### Update a segment
<a name="update-a-segment"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

segment_id = 123456
name = "My New Segment Name"

response = client.segments.update(segment_id, name)
```

### Delete a segment
<a name="delete-a-segment"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

segment_id = 123456

response = client.segments.delete(segment_id)
```

### Get segment information
<a name="get-segment-information"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

segment_id = 123456

response = client.segments.get(segment_id, limit=10, filter={'status': 'active'})
```

### Get subscribers belonging to a segment
<a name="get-subscribers-belonging-to-a-segment"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

segment_id = 123456

response = client.segments.get_subscribers(segment_id, limit=10, filter={'status': 'active'})

next_cursor = response['meta']['next_cursor']
response = client.segments.get_subscribers(segment_id, cursor=next_cursor, limit=10, filter={'status': 'active'})
```

## Fields
<a name="fields"></a>

### List all fields
<a name="list-all-fields"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.fields.list(limit=10, page=1, sort='name', filter={'keyword': 'abc', 'type': 'text'})
```

### Create a field
<a name="create-a-field"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

name = 'My Field'
type = 'text'

response = client.fields.create(name, type)
```

### Update a field
<a name="update-a-field"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

field_id = 123456
name = 'My New Field'

response = client.fields.update(field_id, name)
```

### Delete a field
<a name="delete-a-field"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

field_id = 123456

response = client.fields.delete(field_id)
```

## Automations
<a name="automations"></a>

### List all automations
<a name="list-all-automations"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.automations.list(limit=10, page=1, filter={'enabled': True, 'name': 'some name', 'group': 123456})
```

### Get an automation
<a name="get-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.get(automation_id)
```

### Get subscribers activity for an automation
<a name="get-subscribers-activity-for-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.activity(automation_id, page=1, limit=10, filter={'status': 'active', 'date_from': '2022-12-20', 'date_to': '2022-12-31'})
```

### Create an automation
<a name="create-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.automations.create('My automation')
```

### Update an automation
<a name="update-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.update(automation_id, 'My new name')
```

### Delete an automation
<a name="delete-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.delete(automation_id)
```

### Copy an automation
<a name="copy-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.copy(automation_id)
```

### Enable an automation
<a name="enable-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.enable(automation_id)
```

### Disable an automation
<a name="disable-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.disable(automation_id)
```

### Send a test of an automation
<a name="send-a-test-of-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.test(automation_id, 'some@email.com')
```

### Add subscribers to an automation
<a name="add-subscribers-to-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.add_subscribers(automation_id, emails=['some@email.com'], groups=[1234567])
```

### Re-add subscribers to an automation
<a name="re-add-subscribers-to-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.readd(automation_id, 'last_completed_step', {'status': 'completed'})
```

### Copy automation subscribers to groups
<a name="copy-automation-subscribers-to-groups"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.activity_add_to_group(automation_id, ['1234567'], {'status': 'completed'})
```

### Cancel active automation runs
<a name="cancel-active-automation-runs"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.activity_cancel_automation(automation_id, {'status': 'active'})
```

### Skip an automation delay
<a name="skip-an-automation-delay"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.activity_skip_delay(automation_id, {'status': 'active'})
```

### List automation triggers
<a name="list-automation-triggers"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.list_triggers(automation_id)
```

### Create an automation trigger
<a name="create-an-automation-trigger"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.create_trigger(automation_id, 'subscriber_joins_group', data={'group_ids': [1234567]})
```

### Get an automation trigger
<a name="get-an-automation-trigger"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
trigger_id = 123456

response = client.automations.get_trigger(automation_id, trigger_id)
```

### Update an automation trigger
<a name="update-an-automation-trigger"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
trigger_id = 123456

response = client.automations.update_trigger(automation_id, trigger_id, data={'group_ids': [1234567]})
```

### Delete an automation trigger
<a name="delete-an-automation-trigger"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
trigger_id = 123456

response = client.automations.delete_trigger(automation_id, trigger_id)
```

### List automation steps
<a name="list-automation-steps"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.list_steps(automation_id)
```

### Create an automation step
<a name="create-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.create_step(automation_id, 'delay', parent_id=123456, data={'unit': 'days', 'value': 1})
```

### Get an automation step
<a name="get-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
step_id = 123456

response = client.automations.get_step(automation_id, step_id)
```

### Update an automation step
<a name="update-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
step_id = 123456

response = client.automations.update_step(automation_id, step_id, data={'unit': 'days', 'value': 2})
```

### Delete an automation step
<a name="delete-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
step_id = 123456

response = client.automations.delete_step(automation_id, step_id, branch_to_delete='all')
```

### Copy an automation step
<a name="copy-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
step_id = 123456

response = client.automations.copy_step(automation_id, step_id, parent_id=123456)
```

### Move an automation step
<a name="move-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
step_id = 123456

response = client.automations.reorder_steps(automation_id, step_id, new_parent_step_id=123456)
```

### Select the winner of an A/B test step
<a name="select-the-winner-of-an-ab-test-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
step_id = 123456

response = client.automations.select_ab_test_winner(automation_id, step_id, 'a_path')
```

### Get the content of an automation email
<a name="get-the-content-of-an-automation-email"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
email_id = 123456

response = client.automations.get_email_content(automation_id, email_id)
```

### Update the content of an automation email
<a name="update-the-content-of-an-automation-email"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
email_id = 123456

response = client.automations.update_email_content(automation_id, email_id, '<p>Hello</p>')
```

### Get the report stats of an automation email
<a name="get-the-report-stats-of-an-automation-email"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
email_id = 123456

response = client.automations.email_report_stats(automation_id, email_id, start_date='2026-01-01', end_date='2026-01-31', excel=False)
```

### Get the unsubscribe reasons of an automation email
<a name="get-the-unsubscribe-reasons-of-an-automation-email"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
email_id = 123456

response = client.automations.email_unsubscribe_reasons(automation_id, email_id)
```

### List automation templates
<a name="list-automation-templates"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.automations.list_templates(limit=10, page=1, filter={'category': 1})
```

### Create an automation from a template
<a name="create-an-automation-from-a-template"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

template_id = 123456

response = client.automations.select_template(template_id)
```

### Get the run counts of automation steps
<a name="get-the-run-counts-of-automation-steps"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
step_id = 123456

response = client.automations.steps_run_counts(automation_id)
response = client.automations.step_run_counts(automation_id, step_id)
```

### Get the run counts of automation triggers
<a name="get-the-run-counts-of-automation-triggers"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
trigger_id = 123456

response = client.automations.triggers_run_counts(automation_id)
response = client.automations.trigger_run_counts(automation_id, trigger_id)
```

### Get the stats of A/B test steps
<a name="get-the-stats-of-ab-test-steps"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
step_id = 123456

response = client.automations.ab_steps_stats(automation_id)
response = client.automations.ab_step_stats(automation_id, step_id)
```

### List the subscribers on an automation step
<a name="list-the-subscribers-on-an-automation-step"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
step_id = 123456

response = client.automations.step_subscribers(automation_id, step_id, 'queued', limit=10, page=1)
```

### List the subscribers on an automation trigger
<a name="list-the-subscribers-on-an-automation-trigger"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456
trigger_id = 123456

response = client.automations.trigger_subscribers(automation_id, trigger_id, 'completed', limit=10, page=1)
```

### Get the monthly email totals of an automation
<a name="get-the-monthly-email-totals-of-an-automation"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

automation_id = 123456

response = client.automations.email_monthly_totals(automation_id, start_date='2026-01-01', end_date='2026-06-30')
```

## Campaigns
<a name="campaigns"></a>

### List all campaigns
<a name="list-all-campaigns"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.campaigns.list(limit=10, page=1, filter={'status': 'ready', 'type': 'regular'})
```

### Get a campaign
<a name="get-a-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

campaign_id = 123456

response = client.campaigns.get(campaign_id)
```

### Create a campaign
<a name="create-a-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

params = {
    "name": "Test Campaign",
    "language_id": 1,
    "type": "regular",
    "emails": [{
        "subject": "This is a test campaign",
        "from_name": "Test Man",
        "from": "testuser@mailerlite.com",
        "content": "Hi there, this is a test campaign!"
    }]
}

response = client.campaigns.create(params)
```

### Update a campaign
<a name="update-a-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

campaign_id = 123456
params = {
    "name": "New Campaign Name",
    "language_id": 2,
    "emails": [{
        "subject": "This is a test campaign",
        "from_name": "Test Man",
        "from": "testuser@mailerlite.com",
        "content": "Hi there, this is a test campaign!"
    }]
}

response = client.campaigns.update(campaign_id, params)
```

### Schedule a campaign
<a name="schedule-a-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

campaign_id = 123456
params = {
    "delivery": "scheduled",
    "schedule": {
        "date": "2022-12-31",
        "hours": "22",
        "minutes": "00"
    }
}

response = client.campaigns.schedule(campaign_id, params)
```

### Cancel a campaign
<a name="cancel-a-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

campaign_id = 123456

response = client.campaigns.cancel(campaign_id)
```

### Delete a campaign
<a name="cancel-a-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

campaign_id = 123456

response = client.campaigns.delete(campaign_id)
```

### Get subscribers activity for a campaign
<a name="get-subscribers-activity-for-an-campaign"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

campaign_id = 123456

response = client.campaigns.activity(campaign_id)
```

## Forms
<a name="forms"></a>

### List all forms
<a name="list-all-forms"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.forms.list(limit=10, page=1, sort='name', filter={'name': 'form name'})
```

### Get a form
<a name="get-a-form"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

form_id = 123456

response = client.forms.get(form_id)
```

### Update a form
<a name="update-a-form"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

form_id = 123456
name = 'New Form Name'

response = client.forms.update(form_id, name)
```

### Delete a form
<a name="cancel-a-form"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

form_id = 123456

response = client.forms.delete(form_id)
```

### Get subscribers who signed up to a specific form
<a name="get-subscribers-who-signed-up-to-a-specific-form"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

form_id = 123456

response = client.forms.get_subscribers(form_id, page=1, limit=10, filter={'status': 'active'})
```

## Batching
<a name="batching"></a>

### Create a new batch
<a name="create-a-new-batch"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

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

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.webhooks.list()
```

### Get a webhook
<a name="get-a-webhook"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

webhook_id = 123456

response = client.webhooks.get(webhook_id)
```

### Create a webhook
<a name="create-a-webhook"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

events = [
  'subscriber.created',
  'subscriber.updated',
  'subscriber.unsubscribed'
]
url = 'https://my-url.com'
name = 'Webhook name'

response = client.webhooks.create(events, url, name)
```

### Update a webhook
<a name="update-a-webhook"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

webhook_id = 123456
events = [
  'subscriber.created',
  'subscriber.updated',
  'subscriber.unsubscribed'
]
url = 'https://my-url.com'
name = 'Webhook name'
enabled = False

response = client.webhooks.update(webhook_id, events, url, name, enabled)
```

### Delete a webhook
<a name="cancel-a-webhook"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

webhook_id = 123456

response = client.webhooks.delete(webhook_id)
```

## Timezones
<a name="timezones"></a>

### Get a list of timezones
<a name="get-a-list-of-timezones"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.timezone.list()
```

## Campaign languages
<a name="languages"></a>

### Get a list of languages
<a name="get-a-list-of-languages"></a>

```python
import mailerlite as MailerLite

client = MailerLite.Client({
  'api_key': 'your-api-key'
})

response = client.campaigns.languages()
```
