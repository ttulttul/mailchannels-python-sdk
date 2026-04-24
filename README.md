# MailChannels Python SDK

`mailchannels` is a typed Python SDK for the MailChannels Email API. It is
designed to make the first send small and obvious while still exposing the parts
of MailChannels that matter in production: queued sending through `/send-async`,
sub-account management, templates, unsubscribe behavior, custom headers, and
metrics.

The SDK accepts familiar dictionary payloads for quick scripts and Pydantic
models for codebases that prefer explicit runtime validation.

## Install

Install the SDK with uv:

```bash
uv add mailchannels
```

The synchronous client uses `requests`. Async HTTP support is optional so
applications that do not need it avoid an extra dependency:

```bash
uv add "mailchannels[async]"
```

## Configure The SDK

For small applications and scripts, set the module-level API key once and use
the top-level resources. This mirrors the style of SDKs such as Resend and keeps
common email sends readable.

```python
import mailchannels

mailchannels.api_key = "YOUR-API-KEY"
```

For services that send on behalf of multiple accounts, create explicit clients.
Each client carries its own API key, which is useful when parent-account and
sub-account credentials are both active in the same process.

```python
import mailchannels

parent_client = mailchannels.Client(api_key="PARENT-ACCOUNT-API-KEY")
sub_account_client = mailchannels.Client(api_key="SUB-ACCOUNT-API-KEY")
```

## Send An Email

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

## Queue An Email With `/send-async`

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

## Use Typed Models

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

## Preview With Dry Run

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

## Send A Template Email

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

## Manage DKIM Keys

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

## Add Unsubscribe Support

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

## Add Custom Email Headers

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
        "personalizations": [
            {
                "to": [{"email": "banana-lover@example.net"}],
                "subject": "Bananas Are On Sale",
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

## Async Python

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

## Sub-Accounts

Sub-accounts are a major MailChannels feature, so they are exposed as a
top-level resource. Parent accounts can create sub-accounts, issue API keys,
manage SMTP passwords, set limits, and inspect usage.

```python
sub_account = mailchannels.SubAccounts.create(
    company_name="Client A",
    handle="clienta",
)

api_key = mailchannels.SubAccounts.ApiKeys.create("clienta")
```

Rate limits are useful when each customer, tenant, or downstream sender should
have its own monthly allocation. Set a monthly limit on the sub-account and
MailChannels will enforce that cap independently from the parent account's
overall allocation.

```python
limit = mailchannels.SubAccounts.Limits.set(
    "clienta",
    monthly_limit=100_000,
)

current_limit = mailchannels.SubAccounts.Limits.retrieve("clienta")
```

Usage stats let you show customers how much of their allocation has been used
or decide when to raise, lower, or suspend a limit. Retrieve usage by handle
from the parent account.

```python
usage = mailchannels.SubAccounts.retrieve_usage("clienta")
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

## Metrics

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

## Error Handling

The SDK maps common MailChannels API failures to typed exceptions. Catch the
specific error when your application can respond differently to authentication,
authorization, conflicts, or payload size problems.

```python
try:
    mailchannels.Emails.queue(message)
except mailchannels.PayloadTooLargeError:
    # Reduce attachments or message size before retrying.
    raise
except mailchannels.ForbiddenError:
    # The API key is valid but cannot perform this operation.
    raise
```

All SDK exceptions inherit from `MailChannelsError`.

## Development

Install all development dependencies and run the local test suite:

```bash
uv sync --extra async --extra dev
uv run pytest
```

Current uv releases do not expose `uv pytest` as a native subcommand; use
`uv run pytest` for the portable pytest harness.

Run the suite in SmolVM before committing. In this macOS sandbox, copying a tar
archive into the VM is more reliable than a direct bind mount:

```bash
tar --exclude .venv --exclude .git --exclude dist -cf /tmp/mailchannels-python-sdk.tar .
smolvm machine create mc-sdk-tests --net --image python:3.13-slim
smolvm machine start --name mc-sdk-tests
smolvm machine cp /tmp/mailchannels-python-sdk.tar mc-sdk-tests:/workspace/mailchannels-python-sdk.tar
smolvm machine exec --name mc-sdk-tests -- sh -lc 'cd /workspace && mkdir -p mailchannels-python-sdk && tar -xf mailchannels-python-sdk.tar -C mailchannels-python-sdk && cd mailchannels-python-sdk && pip install uv && uv sync --extra async --extra dev && uv run pytest'
smolvm machine stop --name mc-sdk-tests
```

## License

MIT License. See [LICENSE](LICENSE).
