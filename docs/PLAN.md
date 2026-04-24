# Plan: MailChannels Python SDK

## Goal

Build `mailchannels` as a typed, ergonomic Python SDK for the MailChannels Email
API. Emulate Resend's strongest developer-experience choices: simple setup,
focused resource classes, typed request and response shapes, sync methods plus
`_async` counterparts, optional async dependencies, clear errors, and concise
examples. Adapt the SDK around MailChannels-specific strengths: `/send-async`,
sub-account management, sub-account API keys, SMTP passwords, limits, usage,
webhooks, suppressions, DKIM, and metrics.

## Design Principles

1. Keep the first send path very small.

```python
import mailchannels

mailchannels.api_key = "mc_xxx"

email = mailchannels.Emails.send(
    {
        "from": {"email": "sender@example.com", "name": "Priya Patel"},
        "to": [{"email": "recipient@example.net", "name": "Sakura Tanaka"}],
        "subject": "Hello",
        "text": "Plain text",
        "html": "<strong>Hello</strong>",
    }
)
```

2. Preserve MailChannels-native structure for advanced users.

```python
email = mailchannels.Emails.send(
    mailchannels.EmailParams(
        from_=mailchannels.EmailAddress(email="sender@example.com"),
        personalizations=[
            mailchannels.Personalization(
                to=[mailchannels.EmailAddress(email="recipient@example.net")]
            )
        ],
        subject="Hello",
        content=[mailchannels.Content(type="text/plain", value="Plain text")],
    )
)
```

3. Make `/send-async` first-class without confusing it with Python async.

```python
mailchannels.Emails.send(params)             # sync HTTP, POST /send
await mailchannels.Emails.send_async(params) # async HTTP, POST /send
mailchannels.Emails.queue(params)            # sync HTTP, POST /send-async
await mailchannels.Emails.queue_async(params)# async HTTP, POST /send-async
```

## Package Layout

```text
src/mailchannels/
  __init__.py
  client.py
  config.py
  exceptions.py
  http_client.py
  http_client_async.py
  request.py
  response.py
  emails/
    __init__.py
    emails.py
    types.py
  sub_accounts/
    __init__.py
    sub_accounts.py
    types.py
tests/
examples/
docs/
  LEARNINGS.md
README.md
pyproject.toml
```

## Public API

Core configuration:

```python
mailchannels.api_key = "..."
mailchannels.base_url = "https://api.mailchannels.net/tx/v1"
mailchannels.default_http_client = mailchannels.RequestsClient(timeout=30)
mailchannels.default_async_http_client = mailchannels.HTTPXClient(timeout=30)
```

Email sending:

```python
mailchannels.Emails.send(params, dry_run=False)
mailchannels.Emails.queue(params)
await mailchannels.Emails.send_async(params, dry_run=False)
await mailchannels.Emails.queue_async(params)
```

Sub-account support:

```python
mailchannels.SubAccounts.create(company_name="Client A", handle="clienta")
mailchannels.SubAccounts.list()
mailchannels.SubAccounts.retrieve_usage("clienta")
mailchannels.SubAccounts.suspend("clienta")
mailchannels.SubAccounts.activate("clienta")
mailchannels.SubAccounts.delete("clienta")

mailchannels.SubAccounts.ApiKeys.create("clienta")
mailchannels.SubAccounts.ApiKeys.list("clienta")
mailchannels.SubAccounts.ApiKeys.delete("clienta", key_id)

mailchannels.SubAccounts.SmtpPasswords.create("clienta")
mailchannels.SubAccounts.SmtpPasswords.list("clienta")
mailchannels.SubAccounts.SmtpPasswords.delete("clienta", password_id)

mailchannels.SubAccounts.Limits.set("clienta", monthly_limit=100_000)
mailchannels.SubAccounts.Limits.retrieve("clienta")
mailchannels.SubAccounts.Limits.delete("clienta")
```

Sub-account send ergonomics:

```python
client = mailchannels.Client(api_key="SUB-ACCOUNT-API-KEY")
client.emails.send(params)
client.emails.queue(params)
```

## Typing Strategy

Use Pydantic models for runtime validation and `TypedDict` aliases for
Resend-like dictionary ergonomics. Important types include `EmailAddress`,
`Content`, `Attachment`, `Personalization`, `EmailParams`, `SendResponse`,
`QueuedSendResponse`, `SubAccount`, `SubAccountCreateParams`, `SubAccountLimit`,
`UsageStats`, `ApiKey`, and `SmtpPassword`.

## HTTP And Errors

Implement one request layer with sync and async variants:

- `RequestsClient` for default synchronous HTTP.
- `HTTPXClient` behind the optional `async` extra.
- `MailChannelsError` subclasses for authentication, forbidden access,
  conflicts, payload size, bad gateway, validation, and missing async support.

Map documented MailChannels statuses:

- `/send`: `200`, `202`, `400`, `403`, `413`, `500`, `502`.
- `/send-async`: `202`, `400`, `403`, `413`, `500`.
- `/sub-account`: `201`, `400`, `403`, `409`, `500`.

## Implementation Phases

1. Scaffold the uv package, docs, tests, examples, and typed package marker.
2. Implement configuration, clients, request handling, logging, and exceptions.
3. Implement `/send` and `/send-async` with payload normalization.
4. Implement sub-account lifecycle, API keys, SMTP passwords, limits, and usage.
5. Add suppression, webhook, DKIM, usage, and metrics resources.
6. Expand README examples and integration guidance.
7. Run the full test suite in SmolVM before each commit.
8. Prepare release metadata, package build checks, and CI.
