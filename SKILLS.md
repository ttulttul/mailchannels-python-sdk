# MailChannels Python SDK Usage Guide For LLMs

Use this file when writing, reviewing, or modifying code that consumes the
`mailchannels` Python SDK. Keep examples aligned with the public API exported
from `src/mailchannels`.

## Install And Configure

Install the package with uv:

```bash
uv add mailchannels
```

Install async support only when the application uses async methods:

```bash
uv add "mailchannels[async]"
```

For scripts and simple services, prefer the module-level API:

```python
import mailchannels

mailchannels.api_key = "YOUR-API-KEY"
```

The SDK also reads `MAILCHANNELS_API_KEY` and `MAILCHANNELS_API_URL` from the
environment. Prefer environment variables in deployment examples unless the code
needs multiple clients with different credentials.

For multi-tenant applications, parent accounts, or sub-account sends, prefer
explicit clients so credentials do not get mixed:

```python
parent = mailchannels.Client(api_key="PARENT-API-KEY")
tenant = mailchannels.Client(api_key="SUB-ACCOUNT-API-KEY")
```

## Sending Email

Use `mailchannels.Emails.send()` for synchronous `/send` requests when the
caller wants direct validation feedback.

```python
mailchannels.Emails.send(
    {
        "from": {"email": "sender@example.com", "name": "Sender"},
        "to": [{"email": "recipient@example.net", "name": "Recipient"}],
        "subject": "Hello",
        "text": "Plain text body",
        "html": "<strong>HTML body</strong>",
    }
)
```

Use `mailchannels.Emails.queue()` for `/send-async`. This is the preferred path
for web requests, background jobs, and high-throughput applications.

```python
mailchannels.Emails.queue(
    {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Queued message",
        "text": "Hello",
    }
)
```

Use `send_async()` and `queue_async()` in asyncio applications. Do not call sync
methods from an event loop unless blocking is acceptable. Resource async methods
use the `_async` suffix consistently across emails, DKIM, metrics,
sub-accounts, suppressions, and webhooks.

Responses are dict-like objects with attribute access. It is valid to read
`response["id"]` or `response.id`. HTTP headers are available on
`response.http_headers`.

## Payload Shapes

The SDK accepts compact Resend-style dictionaries and normalizes them into the
MailChannels send shape. For advanced use, pass MailChannels-native
`personalizations` and `content` directly.

```python
mailchannels.Emails.send(
    {
        "from": {"email": "sender@example.com"},
        "personalizations": [
            {"to": [{"email": "recipient@example.net"}]},
        ],
        "subject": "Native payload",
        "content": [{"type": "text/plain", "value": "Hello"}],
    }
)
```

Use Pydantic models when building payloads across multiple functions:

```python
params = mailchannels.EmailParams(
    from_=mailchannels.EmailAddress(email="sender@example.com"),
    personalizations=[
        mailchannels.Personalization(
            to=[mailchannels.EmailAddress(email="recipient@example.net")]
        )
    ],
    subject="Typed message",
    content=[mailchannels.Content(type="text/plain", value="Hello")],
)
```

Use `dry_run=True` with `Emails.send()` when validating rendering, templates, or
headers without delivering a message.

## Templates

MailChannels templates are send-payload fields, not a template CRUD resource.
Set `template_type: "mustache"` on each templated content item and pass
recipient-specific `dynamic_template_data` inside each personalization.

```python
mailchannels.Emails.send(
    {
        "from": {"email": "sender@example.com"},
        "personalizations": [
            {
                "to": [{"email": "jane@example.net"}],
                "dynamic_template_data": {"name": "Jane"},
            }
        ],
        "subject": "Hello",
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

## Unsubscribe

Use `mailchannels.UNSUBSCRIBE_URL_PLACEHOLDER` rather than typing the raw
placeholder by hand. MailChannels requires exactly one recipient per
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
                    f"<a href='{mailchannels.UNSUBSCRIBE_URL_PLACEHOLDER}'>"
                    "unsubscribe</a>"
                ),
                "template_type": "mustache",
            }
        ],
    }
)
```

Set `transactional=False` when requesting native `List-Unsubscribe` headers.
MailChannels requires one recipient per personalization and DKIM signing for
non-transactional messages.

## Custom Headers

Use root `headers` for message-wide custom headers and personalization
`headers` for recipient-specific values. If a header appears in both places,
MailChannels uses the personalization-level value.

Do not set reserved headers such as `From`, `To`, `Subject`, `DKIM-Signature`,
`Message-ID`, or `Content-Type`.

## DKIM

Use `mailchannels.Dkim` or `client.dkim` to manage MailChannels-hosted private
DKIM keys:

```python
key = mailchannels.Dkim.create(
    "example.com",
    selector="mcdkim",
    algorithm="rsa",
    key_length=2048,
)
```

MailChannels hosts the private key, but it does not host public DKIM DNS
records. Always instruct users to publish the returned TXT record in their DNS.
For Cloudflare DNS, use Cloudflare's official Python SDK with a token that has
zone read and DNS edit permissions.

When sending with a MailChannels-hosted key, pass `dkim_domain` and
`dkim_selector`. For customer-managed private keys, also pass the Base64-encoded
`dkim_private_key`.

```python
mailchannels.Emails.queue(
    {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Signed",
        "text": "Signed by DKIM",
        "dkim_domain": "example.com",
        "dkim_selector": "mcdkim",
    }
)
```

## Sub-Accounts

Sub-accounts are first-class. Use them for tenants, customers, or isolated
senders.

```python
mailchannels.SubAccounts.create(company_name="Client A", handle="clienta")
mailchannels.SubAccounts.ApiKeys.create("clienta")
mailchannels.SubAccounts.SmtpPasswords.create("clienta")
```

Document rate limits and usage stats when touching sub-account flows:

```python
mailchannels.SubAccounts.Limits.set("clienta", monthly_limit=100_000)
mailchannels.SubAccounts.Limits.retrieve("clienta")
mailchannels.SubAccounts.retrieve_usage("clienta")
```

When sending with a sub-account API key, create a separate `Client`:

```python
client = mailchannels.Client(api_key="SUB-ACCOUNT-API-KEY")
client.emails.queue({...})
```

## Metrics

Use `mailchannels.Metrics` or `client.metrics` for analytics.

Time-series endpoints:

```python
mailchannels.Metrics.engagement(
    start_time="2026-04-01",
    end_time="2026-04-24T00:00:00Z",
    campaign_id="newsletter",
    interval="day",
)
```

Available methods are `engagement()`, `performance()`,
`recipient_behaviour()`, `recipient_behavior()`, `volume()`, and `senders()`.
Use `senders("campaigns")` or `senders("sub-accounts")` for grouped sender
metrics.

## Suppressions

Use `mailchannels.Suppressions` or `client.suppressions` to list, create, and
delete suppression-list entries.

```python
mailchannels.Suppressions.create(
    [
        {
            "recipient": "recipient@example.net",
            "suppression_types": ["non-transactional"],
            "notes": "Preference-center opt-out",
        }
    ],
    add_to_sub_accounts=True,
)

mailchannels.Suppressions.list(source="api", limit=100)
mailchannels.Suppressions.delete("recipient@example.net", source="all")
```

Use `add_to_sub_accounts=True` when a parent-account suppression should be
copied to sub-accounts.

## Webhooks

Use `mailchannels.Webhooks` or `client.webhooks` to create, list, delete,
validate, inspect, and resend webhook deliveries.

```python
mailchannels.Webhooks.create("https://example.com/mailchannels/events")
mailchannels.Webhooks.validate(request_id="test_request_1")
mailchannels.Webhooks.batches(statuses=["4xx", "5xx"], limit=50)
mailchannels.Webhooks.resend_batch(12345, customer_handle="customer_123")
```

For webhook receivers, use helpers for local checks before processing events:

```python
if not mailchannels.verify_content_digest(headers, raw_body):
    raise ValueError("Invalid MailChannels webhook digest")

key_id = mailchannels.signature_key_id(headers)
parameters = mailchannels.parse_signature_input(headers["Signature-Input"])
if not mailchannels.signature_is_fresh(parameters):
    raise ValueError("Stale MailChannels webhook signature")
```

Fetch unknown public signing keys with `mailchannels.Webhooks.public_key(key_id)`.
Use a dedicated RFC 9421/Ed25519 HTTP-signature verification library for the
final cryptographic signature check.

## Error Handling

Catch specific SDK exceptions when behavior differs by failure type. All SDK
exceptions inherit from `MailChannelsError`.

```python
try:
    mailchannels.Emails.queue(message)
except mailchannels.PayloadTooLargeError:
    raise
except mailchannels.ForbiddenError:
    raise
```

## Repository Maintenance

When adding or changing SDK behavior:

- Update tests for the changed behavior.
- Update `README.md` with user-facing documentation.
- Update this `SKILLS.md` when an LLM would need different guidance.
- Update `docs/LEARNINGS.md` for important discoveries or API semantics.
- Run `uv run pytest`, ruff, build, and the SmolVM pytest workflow before
  committing.
