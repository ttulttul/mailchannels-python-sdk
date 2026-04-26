# MailChannels Python SDK

[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-46aef7.svg)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/ttulttul/mailchannels-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/ttulttul/mailchannels-python-sdk/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/mailchannels)](https://pypi.org/project/mailchannels/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mailchannels)](https://pypi.org/project/mailchannels/)

`mailchannels` is a typed Python SDK for the MailChannels Email API. It keeps
the first send small, then opens up the production features that matter when
email is part of a real product: queued delivery through `/send-async`,
MailChannels-hosted DKIM, domain validation, templates, unsubscribe behavior,
custom headers, metrics, suppressions, and webhooks.

MailChannels is especially strong for multi-tenant sending. Parent accounts can
create isolated sub-accounts, issue separate credentials, set granular limits,
inspect usage, and keep one customer's bad traffic from endangering the parent
account or other tenants. Behind the API, MailChannels applies sophisticated
spam and phishing filtering, automatically using fine-grained rate limits and
blocks to contain abusive or compromised senders without treating all traffic as
one shared risk pool.

The SDK accepts familiar dictionary payloads for quick scripts and Pydantic
models for codebases that prefer explicit runtime validation. Use the
module-level resources when you want Resend-style convenience; create explicit
`Client` instances when each tenant, account, or service needs its own
credentials.

## Start Here

- New to the SDK: start with [Five-Minute Quickstart](#five-minute-quickstart).
- Building a sending workflow: use [Common Sending Recipes](#common-sending-recipes).
- Building a multi-tenant product: read [Account And Domain Operations](#account-and-domain-operations).
- Operating at scale: jump to [Production Operations](#production-operations).
- Maintaining the SDK: see [Development](#development).

## Five-Minute Quickstart

### Install

Install the SDK with uv:

```bash
uv add mailchannels
```

The synchronous client uses `requests`. Async HTTP support is optional so
applications that do not need it avoid an extra dependency:

```bash
uv add "mailchannels[async]"
```

### Configure

For small applications and scripts, set the module-level API key once and use
the top-level resources. This mirrors the style of SDKs such as Resend and keeps
common email sends readable.

```python
import mailchannels

mailchannels.api_key = "YOUR-API-KEY"
```

The SDK also reads `MAILCHANNELS_API_KEY` and `MAILCHANNELS_API_URL` from the
environment. Environment variables are the cleanest option for deployed
services because the same code can run in development, staging, and production
without committing credentials or hostnames.

```bash
export MAILCHANNELS_API_KEY="YOUR-API-KEY"
```

For services that send on behalf of multiple accounts, create explicit clients.
Each client carries its own API key, which is useful when parent-account and
sub-account credentials are both active in the same process.

```python
import mailchannels

parent_client = mailchannels.Client(api_key="PARENT-ACCOUNT-API-KEY")
sub_account_client = mailchannels.Client(api_key="SUB-ACCOUNT-API-KEY")
```

### Send

The quickest path is `Emails.send()`. It performs a synchronous HTTP request to
MailChannels and returns the API response after the message has been accepted.
Use this when you want immediate validation feedback from the send endpoint.

```python
import mailchannels

mailchannels.api_key = "YOUR-API-KEY"

email = mailchannels.Emails.send(
    {
        "from": {"email": "sender@example.com", "name": "Priya Patel"},
        "to": [{"email": "recipient@example.net", "name": "Sakura Tanaka"}],
        "subject": "Testing Email API",
        "text": "Hi Sakura. This is just a test from Priya.",
    }
)

print(email)
```

The SDK normalizes this compact payload into the MailChannels send shape. For
advanced messages, you can pass MailChannels-native `personalizations` and
`content` directly.

```python
email = mailchannels.Emails.send(
    {
        "from": {"email": "sender@example.com"},
        "personalizations": [
            {"to": [{"email": "recipient@example.net"}]},
        ],
        "subject": "Native payload",
        "content": [
            {"type": "text/plain", "value": "Plain text body"},
            {"type": "text/html", "value": "<strong>HTML body</strong>"},
        ],
    }
)
```

### Queue With `/send-async`

MailChannels has a first-class asynchronous processing endpoint. Use
`Emails.queue()` when your application should hand the message to MailChannels
quickly and continue without waiting for the regular send path. The payload is
the same as `Emails.send()`, but the SDK posts it to `/send-async`.

```python
queued = mailchannels.Emails.queue(
    {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Queued message",
        "html": "<strong>Hello</strong>",
    }
)
```

This is usually the better default for high-throughput web applications, job
workers, or any path where email should not slow down the user-facing request.

## Core Concepts

### API Coverage

The SDK covers the MailChannels Email API surfaces that production senders need
most often:

- Email sending through `/send` and queued sending through `/send-async`.
- Domain validation through `POST /check-domain`, exposed as
  `mailchannels.CheckDomain` and `client.check_domain`.
- MailChannels-hosted DKIM key creation, listing, status updates, and rotation.
- Sub-account creation, suspension, activation, credentials, singular
  `/sub-account/{handle}/limit` rate limits, and usage stats.
- Templates, unsubscribe metadata, custom email headers, suppression lists,
  metrics, usage, and webhooks.

| Need | Endpoint | SDK surface |
| --- | --- | --- |
| Send now | `POST /send` | `mailchannels.Emails.send()` |
| Queue for processing | `POST /send-async` | `mailchannels.Emails.queue()` |
| Validate sender DNS and lockdown | `POST /check-domain` | `mailchannels.CheckDomain.check()` |
| Manage hosted DKIM keys | `/domains/{domain}/dkim-keys` | `mailchannels.Dkim` |
| Isolate tenants | `/sub-account` | `mailchannels.SubAccounts` |
| Cap tenant volume | `/sub-account/{handle}/limit` | `mailchannels.SubAccounts.Limits` |
| Inspect traffic health | `/metrics/*` | `mailchannels.Metrics` |
| Manage suppressions | `/suppression-list` | `mailchannels.Suppressions` |
| Receive delivery events | `/webhook*` | `mailchannels.Webhooks` |

Route coverage is guarded in three layers. The normal test tree includes
`tests/test_openapi_contract.py`, which checks exact agreement between SDK
route declarations and a local OpenAPI route snapshot.
`tests/test_openapi_request_contract.py` executes every declared route through a
fake transport and validates the emitted method, path, JSON keys, query keys,
and operation-specific headers against the documented request shape; it also
asserts the sync and async variants emit identical requests. CI also runs
`scripts/check_openapi_drift.py`, which parses and validates the official
MailChannels OpenAPI document with `openapi-spec-validator` before comparing
its routes with the SDK route registry in both directions. That catches stale
SDK routes, newly documented endpoints, async drift, and subtle request-shape
drift before it lands on `main`.

### Choosing The Right Entry Point

| Use this | When it fits |
| --- | --- |
| `mailchannels.Emails.send()` | You want synchronous validation from `/send`. |
| `mailchannels.Emails.queue()` | You want fast handoff to `/send-async`; this is usually best for web requests and workers. |
| `mailchannels.CheckDomain.check()` | You are onboarding or troubleshooting a sending domain. |
| `mailchannels.Dkim` | You need MailChannels to create, store, rotate, or validate hosted DKIM keys. |
| `mailchannels.SubAccounts` | You send for multiple tenants and need isolation, credentials, usage, or limits per tenant. |
| Explicit `mailchannels.Client(...)` | You need different API keys, base URLs, or HTTP transports in the same process. |

### Read Responses

SDK responses behave like ordinary dictionaries, but they also support
attribute access for the common case where you want to read one or two fields.
HTTP response headers are preserved under `http_headers` for diagnostics,
request IDs, and future rate-limit metadata.

```python
queued = mailchannels.Emails.queue(message)

print(queued["id"])
print(queued.id)
print(queued.http_headers)
```

Set `strict_responses=True` when you want modeled endpoints to return Pydantic
response objects instead. Strict mode validates the API response body against
the SDK's response model and raises `ResponseValidationError` if the response no
longer matches the expected shape. Endpoints without a stable model still return
the normal dict-like response.

```python
client = mailchannels.Client(
    api_key="YOUR-API-KEY",
    strict_responses=True,
)

usage = client.usage.retrieve()

print(usage.total_usage)
print(usage.http_headers)
```

### Use Typed Models

Dictionary payloads are convenient, but long-lived applications often benefit
from explicit types. `EmailParams`, `EmailAddress`, `Content`, and
`Personalization` are Pydantic models that validate the request before it reaches
the HTTP layer.

```python
params = mailchannels.EmailParams(
    from_=mailchannels.EmailAddress(email="sender@example.com"),
    personalizations=[
        mailchannels.Personalization(
            to=[mailchannels.EmailAddress(email="recipient@example.net")]
        )
    ],
    subject="Typed message",
    content=[
        mailchannels.Content(type="text/plain", value="Hello from typed models.")
    ],
)

mailchannels.Emails.send(params)
```

Use typed models when you are constructing messages across several functions or
want validation errors to appear close to the code that builds the payload.

## Common Sending Recipes

### Add Attachments

MailChannels expects attachment content to be Base64 encoded. The SDK's
`Attachment` helper handles that encoding for local files or bytes, infers a
MIME type from the filename, and preserves the MailChannels fields in the final
send payload.

```python
invoice = mailchannels.Attachment.from_file("invoice.pdf")

mailchannels.Emails.queue(
    {
        "from": {"email": "billing@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Your invoice",
        "text": "Your invoice is attached.",
        "attachments": [invoice],
    }
)
```

Inline attachments use the same encoded payload but set `disposition` to
`inline` and provide a `content_id`. Reference that content ID from your HTML
with a `cid:` URL.

```python
logo = mailchannels.Attachment.inline_file(
    "logo.png",
    content_id="company-logo",
)

mailchannels.Emails.queue(
    {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Inline image",
        "html": "<img src='cid:company-logo' alt='Company logo'>",
        "attachments": [logo],
    }
)
```

Use `Attachment.from_bytes()` when the file is generated in memory, such as a
PDF created by your application. Use `Attachment.from_url()` when the attachment
already lives behind an HTTP URL and you want the SDK to fetch and encode it
before sending.

### Preview With Dry Run

MailChannels supports dry-run validation on the send endpoint. Pass
`dry_run=True` to send the request for validation and rendering checks without
actually delivering the message.

```python
preview = mailchannels.Emails.send(
    {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Dry run",
        "text": "Validate this message without delivering it.",
    },
    dry_run=True,
)
```

Dry runs are especially useful when testing templates, headers, and unsubscribe
behavior.

### Send A Template Email

MailChannels templates are part of the send payload rather than a separate
template CRUD API. Mark each templated content part with
`template_type: "mustache"` and provide recipient-specific values in
`dynamic_template_data`.

```python
preview = mailchannels.Emails.send(
    {
        "from": {"email": "sender@example.com"},
        "personalizations": [
            {
                "to": [{"email": "jane@example.net"}],
                "dynamic_template_data": {"name": "Jane Doe"},
            },
            {
                "to": [{"email": "john@example.net"}],
                "dynamic_template_data": {"name": "John Smith"},
            },
        ],
        "subject": "Template Example",
        "content": [
            {
                "type": "text/plain",
                "value": "Hello {{name}}",
                "template_type": "mustache",
            }
        ],
    },
    dry_run=True,
)
```

The example renders a different greeting for each recipient. `dry_run=True`
keeps the example safe while you confirm the final rendered content.

### Manage DKIM Keys

MailChannels can generate and store DKIM private keys for your account. This is
the easiest way to avoid handling private key material in your own application:
create a key pair with the DKIM API, publish the returned public DNS record, and
then reference the selector when sending.

```python
key = mailchannels.Dkim.create(
    "example.com",
    selector="mcdkim",
    algorithm="rsa",
    key_length=2048,
)

for record in key.get("dkim_dns_records", []):
    print(record["name"], record["type"], record["value"])
```

MailChannels hosts the private key used for signing. At this time,
MailChannels does not host DKIM public keys for your domain; you must copy the
returned public DKIM TXT record into your own DNS zone. The TXT record name will
look like `mcdkim._domainkey.example.com`.

If your DNS is hosted in Cloudflare, you can publish the returned DKIM TXT
record with Cloudflare's official Python SDK. The example below uses
`CLOUDFLARE_API_TOKEN` from the environment, finds the zone, updates an existing
TXT record when it is present, and creates it when it is missing.

```bash
uv add cloudflare
export CLOUDFLARE_API_TOKEN="your_cloudflare_api_token"
```

```python
from cloudflare import Cloudflare

import mailchannels


DOMAIN = "example.com"
SELECTOR = "mcdkim"

mailchannels.api_key = "YOUR-MAILCHANNELS-API-KEY"
cloudflare = Cloudflare()


def publish_mailchannels_dkim_record() -> None:
    """Create a MailChannels DKIM key and publish its public key in Cloudflare."""
    key = mailchannels.Dkim.create(
        DOMAIN,
        selector=SELECTOR,
        algorithm="rsa",
        key_length=2048,
    )
    dns_record = key["dkim_dns_records"][0]

    zones = cloudflare.zones.list(name=DOMAIN)
    zone = next(iter(zones), None)
    if zone is None:
        raise RuntimeError(f"Cloudflare zone not found: {DOMAIN}")

    records = cloudflare.dns.records.list(
        zone_id=zone.id,
        type="TXT",
        name=dns_record["name"],
    )
    existing_record = next(iter(records), None)

    if existing_record is None:
        updated_record = cloudflare.dns.records.create(
            zone_id=zone.id,
            type="TXT",
            name=dns_record["name"],
            content=dns_record["value"],
            ttl=1,
        )
    else:
        updated_record = cloudflare.dns.records.update(
            existing_record.id,
            zone_id=zone.id,
            type="TXT",
            name=dns_record["name"],
            content=dns_record["value"],
            ttl=1,
        )

    print(f"Published DKIM record: {updated_record.name}")


publish_mailchannels_dkim_record()
```

The Cloudflare token needs permission to read the zone and edit DNS records. In
Cloudflare's dashboard, grant at least `Zone: Read` and `DNS: Edit` for the
zone that owns the sending domain.

After the DNS record is published, send mail with the selector. If
`dkim_domain` is omitted, MailChannels can derive it from the `from` address,
but setting it explicitly keeps the signing intent obvious.

```python
mailchannels.Emails.queue(
    {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "DKIM signed message",
        "text": "This message is signed by a MailChannels-hosted DKIM key.",
        "dkim_domain": "example.com",
        "dkim_selector": "mcdkim",
    }
)
```

You can retrieve keys, include the suggested DNS record in the response, update
key status, and rotate active keys. Rotation creates a replacement key and
returns the DNS record you need to publish before switching all signing traffic
to the new selector.

```python
keys = mailchannels.Dkim.list("example.com", include_dns_record=True)
rotated = mailchannels.Dkim.rotate(
    "example.com",
    "mcdkim",
    new_selector="mcdkim2",
)
mailchannels.Dkim.update_status("example.com", "mcdkim", status="rotated")
```

If you manage your own DKIM keys instead, pass `dkim_domain`, `dkim_selector`,
and the Base64-encoded `dkim_private_key` in the send payload. Values set inside
a personalization override root-level DKIM values for that recipient.

### Add Unsubscribe Support

MailChannels can render a hosted one-click unsubscribe URL inside mustache
content. Use the exported `UNSUBSCRIBE_URL_PLACEHOLDER` constant so the
placeholder is not mistyped. MailChannels requires exactly one recipient per
personalization when unsubscribe links are used.

```python
mailchannels.Emails.queue(
    {
        "from": {"email": "sender@example.com"},
        "personalizations": [{"to": [{"email": "recipient@example.net"}]}],
        "subject": "Newsletter",
        "content": [
            {
                "type": "text/html",
                "value": (
                    "<p>Hello</p>"
                    f"<a href='{mailchannels.UNSUBSCRIBE_URL_PLACEHOLDER}'>"
                    "unsubscribe</a>"
                ),
                "template_type": "mustache",
            }
        ],
    }
)
```

For automatic `List-Unsubscribe` headers, set `transactional` to `False`.
MailChannels documents that this mode also requires one recipient per
personalization and DKIM signing.

```python
mailchannels.Emails.queue(
    {
        "from": {"email": "sender@example.com"},
        "personalizations": [
            {
                "to": [{"email": "recipient@example.net"}],
                "dkim_domain": "example.com",
                "dkim_selector": "mailchannels",
                "dkim_private_key": "-----BEGIN PRIVATE KEY-----...",
            }
        ],
        "subject": "Newsletter",
        "text": "Hello",
        "transactional": False,
    }
)
```

### Add Custom Email Headers

Use `headers` when a message needs additional email headers such as campaign
metadata, unsubscribe hints, or application-specific tracking values.
MailChannels may reject restricted or duplicate headers, so prefer a small,
intentional set.

```python
mailchannels.Emails.send(
    {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Custom Header Example",
        "text": "This email includes custom headers.",
        "headers": {
            "List-Unsubscribe": "<mailto:unsubscribe@example.com>",
            "X-Campaign-ID": "newsletter-123",
        },
    }
)
```

Headers can also be set per personalization. This is useful when each recipient
needs a different value. If the same header exists globally and on a
personalization, MailChannels uses the personalization-level value.

```python
mailchannels.Emails.send(
    {
        "from": {"email": "sender@example.com"},
        "subject": "Bananas Are On Sale",
        "personalizations": [
            {
                "to": [{"email": "banana-lover@example.net"}],
                "headers": {
                    "List-Unsubscribe": "<mailto:unsubscribe@bananas.example>",
                    "X-Custom-Header": "BananaFan123",
                },
            }
        ],
        "content": [
            {
                "type": "text/plain",
                "value": "This email includes custom headers.",
            }
        ],
    }
)
```

### Async Python

Async methods use the same payloads as the synchronous methods and are named
with the `_async` suffix. Use them in FastAPI, Starlette, aiohttp workers, or
other asyncio applications where blocking the event loop would be the wrong
tradeoff.

```python
import asyncio
import mailchannels

mailchannels.api_key = "YOUR-API-KEY"


async def main() -> None:
    queued = await mailchannels.Emails.queue_async(
        {
            "from": {"email": "sender@example.com"},
            "to": [{"email": "recipient@example.net"}],
            "subject": "Queued message",
            "text": "Hello",
        }
    )
    print(queued)


asyncio.run(main())
```

Install `mailchannels[async]` before using async methods.

## Account And Domain Operations

### Sub-Accounts

Sub-accounts are a major MailChannels feature, so they are exposed as a
top-level resource. Parent accounts can create sub-accounts, issue API keys,
manage SMTP passwords, set limits, and inspect usage.

```python
sub_account = mailchannels.SubAccounts.create(
    company_name="Client A",
    handle="clienta",
)

sub_accounts = mailchannels.SubAccounts.list(limit=100, offset=0)
api_key = mailchannels.SubAccounts.ApiKeys.create("clienta")
```

Rate limits are useful when each customer, tenant, or downstream sender should
have its own monthly allocation. Set a monthly limit on the sub-account and
MailChannels will enforce that cap independently from the parent account's
overall allocation.

```python
limit = mailchannels.SubAccounts.Limits.set(
    "clienta",
    sends=100_000,
)

current_limit = mailchannels.SubAccounts.Limits.retrieve("clienta")
```

Usage stats let you show customers how much of their allocation has been used
or decide when to raise, lower, or suspend a limit. Retrieve usage by handle
from the parent account.

```python
usage = mailchannels.SubAccounts.retrieve_usage("clienta")
```

The parent account also has its own top-level usage endpoint. Use it when you
need the current billing-period total for the account represented by the API key
rather than for one specific sub-account.

```python
usage = mailchannels.Usage.retrieve()

print(usage.total_usage)
print(usage.period_start_date, usage.period_end_date)
```

If you want the sub-account to inherit the parent account's remaining capacity
again, delete the explicit sub-account limit.

```python
mailchannels.SubAccounts.Limits.delete("clienta")
```

When sending as a sub-account, create a separate client with that sub-account's
API key. This keeps account boundaries explicit in code.

```python
client = mailchannels.Client(api_key="SUB-ACCOUNT-API-KEY")
client.emails.queue(
    {
        "from": {"email": "sender@client.example"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Client message",
        "text": "Hello",
    }
)
```

### Domain Checks

Before sending from a domain, you can ask MailChannels to verify the domain's
authentication posture. `CheckDomain.check()` and `DomainChecks.check()` both
call `/check-domain` and return the API's DKIM, SPF, sender-domain DNS, and
Domain Lockdown results. This is useful in setup flows where you want to tell a
user exactly which DNS or DKIM step is still missing. Client instances expose
the same operation as `client.check_domain.check(...)`; `client.domain_checks`
is kept as a plural alias for consistency with the result set.

```python
result = mailchannels.CheckDomain.check("example.com")

print(result.check_results["spf"]["verdict"])
print(result.references)
```

If you use MailChannels-hosted DKIM keys, pass the selector you expect the
domain to use. MailChannels will validate the stored key for that domain and
selector.

```python
result = mailchannels.CheckDomain.check(
    "example.com",
    dkim_settings=[
        mailchannels.DkimSetting(
            dkim_domain="example.com",
            dkim_selector="mcdkim",
        )
    ],
)
```

## Production Operations

### Metrics

Metrics endpoints expose the operational view of your email traffic. Use them
to build dashboards, reconcile campaign performance, or monitor sender health.
The time-series endpoints accept `start_time`, `end_time`, `campaign_id`, and
`interval`.

```python
engagement = mailchannels.Metrics.engagement(
    start_time="2026-04-01",
    end_time="2026-04-24T00:00:00Z",
    campaign_id="newsletter",
    interval="day",
)
```

Sender metrics group results by campaigns or sub-accounts and support ordinary
pagination controls.

```python
senders = mailchannels.Metrics.senders(
    "sub-accounts",
    limit=50,
    offset=0,
    sort_order="desc",
)
```

Available metrics methods are `engagement()`, `performance()`,
`recipient_behaviour()`, `recipient_behavior()`, `volume()`, and `senders()`.

### Suppression Lists

Suppression lists are the MailChannels-native way to keep known unwanted
recipients out of future sends. The SDK exposes list, create, and delete
operations. Use them when you need to import suppressions from your own product,
inspect automatically generated hard-bounce or complaint suppressions, or remove
an address after a user explicitly opts back in.

```python
mailchannels.Suppressions.create(
    [
        {
            "recipient": "recipient@example.net",
            "suppression_types": ["non-transactional"],
            "notes": "Imported from billing system preference center.",
        }
    ],
    add_to_sub_accounts=True,
)

entries = mailchannels.Suppressions.list(
    source="api",
    limit=100,
)

mailchannels.Suppressions.delete("recipient@example.net", source="all")
```

`add_to_sub_accounts=True` is useful for parent-account workflows where one
suppression should be copied across the tenant accounts beneath it.

### Webhooks

MailChannels can send delivery events to your application for accepted,
delivered, bounced, opened, clicked, complained, and unsubscribed messages. The
SDK exposes webhook enrollment, validation, batch inspection, batch resend, and
public signing-key retrieval.

```python
mailchannels.Webhooks.create("https://example.com/mailchannels/events")

validation = mailchannels.Webhooks.validate(request_id="test_request_1")
batches = mailchannels.Webhooks.batches(statuses=["4xx", "5xx"], limit=50)

mailchannels.Webhooks.resend_batch(
    12345,
    customer_handle="customer_123",
)
```

Webhook receivers should verify the `customer_handle` in each event and check
the signature headers MailChannels sends with the request. The SDK includes
small helpers for the local pieces that can be done without extra crypto
dependencies: parsing `Signature-Input`, extracting the key ID, checking replay
age, and verifying the `Content-Digest` against the raw request body.

```python
from mailchannels import (
    parse_signature_input,
    signature_is_fresh,
    signature_key_id,
    verify_content_digest,
)


def receive_webhook(headers: dict[str, str], body: bytes) -> None:
    """Validate local webhook metadata before processing events."""
    if not verify_content_digest(headers, body):
        raise ValueError("Invalid MailChannels webhook digest")

    key_id = signature_key_id(headers)
    public_key = mailchannels.Webhooks.public_key(key_id) if key_id else None

    parameters = parse_signature_input(headers["Signature-Input"])
    if not signature_is_fresh(parameters, tolerance_seconds=300):
        raise ValueError("Stale MailChannels webhook signature")

    # Use `public_key["key"]` with an RFC 9421/Ed25519 verification library.
```

MailChannels signs webhooks with Ed25519 and documents the signing flow in terms
of RFC 9421. This SDK intentionally leaves the final cryptographic verification
step to a dedicated HTTP-signature library so application code can choose the
verification package that fits its web framework.

### Error Handling

The SDK maps common MailChannels API failures to typed exceptions. Catch the
specific error when your application can respond differently to authentication,
authorization, invalid requests, rate limits, conflicts, payload size problems,
or server-side failures.

```python
try:
    mailchannels.Emails.queue(message)
except mailchannels.PayloadTooLargeError:
    # Reduce attachments or message size before retrying.
    raise
except mailchannels.ForbiddenError:
    # The API key is valid but cannot perform this operation.
    raise
except mailchannels.RateLimitError:
    # Back off before retrying; inspect error.retry_after if present.
    raise
except mailchannels.InvalidRequestError:
    # Fix request parameters or payload shape before retrying.
    raise
except mailchannels.ServerError:
    # Retry later or contact support with error.request_id.
    raise
```

All API response exceptions inherit from `ApiError`, and all SDK exceptions
inherit from `MailChannelsError`.

Each exception carries structured metadata for logs and support workflows:
`status_code`, `code`, `error_type`, `headers`, `request_id`, `retry_after`,
`suggested_action`, and the parsed API `response`. Use `to_dict()` when you want
to send consistent error metadata to your logger.

```python
try:
    mailchannels.Emails.queue(message)
except mailchannels.MailChannelsError as error:
    logger.error("MailChannels request failed", extra=error.to_dict())
    raise
```

### Version And Custom Transports

The package exports its version so applications can log it at startup or include
it in diagnostics. The SDK uses the same value in its `User-Agent` header.

```python
import mailchannels

print(mailchannels.__version__)
print(mailchannels.get_version())
```

The default synchronous transport uses `requests`, and the default async
transport uses `httpx`. If your application needs custom retry behavior,
instrumentation, test isolation, or a framework-specific HTTP stack, pass a
transport object that implements the `SyncHTTPClient` or `AsyncHTTPClient`
protocol. The method must return `mailchannels.SDKResponse`.

```python
from typing import Any

import mailchannels


class LoggingTransport:
    """Small example transport that satisfies SyncHTTPClient."""

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> mailchannels.SDKResponse:
        """Send a request and return a normalized SDK response."""
        print(method, url)
        return mailchannels.RequestsClient().request(
            method,
            url,
            headers=headers,
            json=json,
            params=params,
        )


client = mailchannels.Client(
    api_key="YOUR-API-KEY",
    http_client=LoggingTransport(),
)
```

## Examples

The `examples/` directory contains tested, focused examples for common
production tasks:

- `async_email.py` queues a message with the async transport.
- `attachments.py` sends local, generated, and inline attachments.
- `templates.py` builds and dry-runs mustache template messages.
- `unsubscribe.py` builds one-click and automatic List-Unsubscribe messages.
- `custom_headers.py` sends global and per-recipient custom email headers.
- `dkim.py` creates, lists, and rotates MailChannels-hosted DKIM keys.
- `cloudflare_dkim.py` publishes MailChannels DKIM TXT records in Cloudflare.
- `sub_accounts.py` creates sub-accounts, credentials, limits, and usage views.
- `metrics.py` retrieves engagement and sender metrics.
- `domain_checks.py` validates DKIM, SPF, sender-domain DNS, and Domain Lockdown
  status for a sending domain.
- `suppressions.py` creates, lists, and deletes suppression entries.
- `webhooks.py` configures webhooks and verifies local webhook metadata.
- `usage.py` retrieves parent-account and sub-account usage.
- `custom_http_client.py` wraps a custom transport.
- `error_handling.py` logs structured SDK exception metadata.

The README's fenced Python snippets are also syntax-checked and smoke-tested
with fake SDK transports so documentation examples stay aligned with executable
SDK behavior without calling the live MailChannels API.

## Development

Install all development dependencies and run the local test suite:

```bash
uv sync --extra async --extra dev
uv run pytest
uv run pytest --cov --cov-report=term-missing
uv run ruff check src tests examples scripts typing_tests
uv run mypy
uv run python scripts/run_consumer_typing.py
uv build
uv run python scripts/smoke_wheel_install.py
uv run python scripts/check_openapi_drift.py
```

Current uv releases do not expose `uv pytest` as a native subcommand; use
`uv run pytest` for the portable pytest harness.

The GitHub Actions CI workflow runs the same checks on pushes to `main`, pull
requests, and manual dispatches. It runs pytest across Python 3.9 through 3.13
and enforces an 85% branch coverage threshold on Python 3.13. It also compares
the SDK's declared routes with the official MailChannels OpenAPI spec so
documented endpoint changes are caught early. The unit test suite includes
direct transport-wrapper tests and explicit API error mapping tests so request
forwarding, non-JSON responses, headers, timeouts, and exception metadata stay
stable. It also extracts README Python snippets and executes the safe examples
against fake transports so user documentation cannot quietly drift from the
SDK. CI type-checks a small external-consumer fixture and installs the built
wheel into clean environments with and without the `[async]` extra. The separate
online API workflow is manual-only and expects
`MAILCHANNELS_API_KEY` as a GitHub secret plus optional repository or environment
variables for sender, recipient, DKIM domain, and API URL.

The PyPI publishing workflow builds, tests, type-checks, validates OpenAPI
drift, runs `twine check`, and publishes the verified `dist/` artifact through
PyPI trusted publishing. Configure PyPI with a trusted publisher for
`.github/workflows/publish.yml` and the GitHub environment `pypi`. Push a
version tag such as `v0.1.0`, matching `pyproject.toml`, to publish
automatically, or run the workflow manually with `publish=true`.

### Online API Tests

The default test suite never calls the live MailChannels API. Online tests are
marked with `online` and run only when you both provide a real API key in the
environment and pass `--online`.

```bash
export MAILCHANNELS_API_KEY="your_real_mailchannels_api_key"
uv run pytest -m online --online
```

The online suite includes parent-account usage, async usage, volume metrics,
sub-account listing, suppression listing, webhook listing, and optional domain
checks and DKIM listing. The volume metrics test sends an explicit 24-hour
`start_time` and `end_time` window so the live service does not need to infer an
unbounded range. It can also validate the send endpoint with a MailChannels dry
run, which does not deliver a message. Set sender and recipient addresses to
enable that dry-run test:

```bash
export MAILCHANNELS_ONLINE_FROM="sender@example.com"
export MAILCHANNELS_ONLINE_TO="recipient@example.net"
uv run pytest -m online --online
```

To run the optional `/check-domain` and DKIM listing tests, provide a domain
that belongs to the account:

```bash
export MAILCHANNELS_ONLINE_DOMAIN="example.com"
uv run pytest -m online --online
```

The suite also includes a test that sends a real email through `/send`. It is
disabled unless you explicitly opt in with `MAILCHANNELS_ONLINE_SEND_REAL=1`:

```bash
export MAILCHANNELS_ONLINE_FROM="sender@example.com"
export MAILCHANNELS_ONLINE_TO="recipient@example.net"
export MAILCHANNELS_ONLINE_SEND_REAL=1
uv run pytest tests/test_online_api.py::test_online_send_real_email --online
```

Use `MAILCHANNELS_API_URL` if you need to point the online tests at a non-default
MailChannels API host.

If the live MailChannels service returns a 5xx response, times out, or drops a
connection for an online endpoint, that test is reported as `xfail` because the
failure is outside the local SDK behavior being tested. Authentication and
authorization errors still fail the test normally.

Destructive online CRUD tests are marked `online_destructive` and stay disabled
unless you pass both `--online` and `--online-destructive` and set
`MAILCHANNELS_ONLINE_DESTRUCTIVE=1`. Run these only against a dedicated test
account because they create and delete suppressions, sub-accounts, credentials,
limits, and webhook configuration. The MailChannels webhook delete endpoint
removes all configured webhooks.

```bash
export MAILCHANNELS_ONLINE_DESTRUCTIVE=1
uv run pytest -m online_destructive --online --online-destructive
```

Run the suite in SmolVM before committing. In this macOS sandbox, copying a tar
archive into the VM is more reliable than a direct bind mount:

```bash
COPYFILE_DISABLE=1 tar --exclude .venv --exclude .git --exclude dist --exclude .mypy_cache --exclude .ruff_cache --exclude .pytest_cache -cf /tmp/mailchannels-python-sdk.tar .
smolvm machine create mc-sdk-tests --net --image python:3.13-slim
smolvm machine start --name mc-sdk-tests
smolvm machine cp /tmp/mailchannels-python-sdk.tar mc-sdk-tests:/workspace/mailchannels-python-sdk.tar
smolvm machine exec --name mc-sdk-tests -- sh -lc 'cd /workspace && mkdir -p mailchannels-python-sdk && tar -xf mailchannels-python-sdk.tar -C mailchannels-python-sdk && cd mailchannels-python-sdk && pip install uv && uv sync --extra async --extra dev && uv run pytest'
smolvm machine stop --name mc-sdk-tests
```

## License

MIT License. See [LICENSE](LICENSE).
