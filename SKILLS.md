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

## Attachments

Use `mailchannels.Attachment.from_file()` for local files,
`Attachment.from_bytes()` for generated content, and `Attachment.from_url()` for
remote HTTP objects. These helpers Base64 encode the content and infer the MIME
type from the filename or response headers.

```python
mailchannels.Emails.queue(
    {
        "from": {"email": "sender@example.com"},
        "to": [{"email": "recipient@example.net"}],
        "subject": "Report",
        "text": "Attached.",
        "attachments": [
            mailchannels.Attachment.from_file("report.pdf"),
        ],
    }
)
```

For inline images, use `Attachment.inline_file(path, content_id="...")` and
reference the content ID from HTML with `cid:...`.

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
mailchannels.SubAccounts.list(limit=100, offset=0)
mailchannels.SubAccounts.ApiKeys.create("clienta")
mailchannels.SubAccounts.SmtpPasswords.create("clienta")
```

Document rate limits and usage stats when touching sub-account flows:

```python
mailchannels.SubAccounts.Limits.set("clienta", sends=100_000)
mailchannels.SubAccounts.Limits.retrieve("clienta")
mailchannels.SubAccounts.retrieve_usage("clienta")
mailchannels.Usage.retrieve()
```

Sub-account limit endpoints must use singular `/sub-account/{handle}/limit`.
Setting a limit must send `PUT` with a `sends` payload. The SDK still accepts
`monthly_limit` as a compatibility alias, but examples and docs should prefer
`sends`.

## Domain Checks

Use `mailchannels.CheckDomain` or `client.check_domain` for `/check-domain`.
`mailchannels.DomainChecks` and `client.domain_checks` remain supported aliases.
This endpoint checks DKIM, SPF, sender-domain DNS, and Domain Lockdown status:

```python
mailchannels.CheckDomain.check("example.com")
mailchannels.CheckDomain.check(
    "example.com",
    dkim_settings=[mailchannels.DkimSetting(dkim_selector="mcdkim")],
)
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

## Usage

Use `mailchannels.Usage.retrieve()` or `client.usage.retrieve()` for
parent-account usage during the current billing period. Use
`SubAccounts.retrieve_usage(handle)` only when asking about one sub-account.

```python
usage = mailchannels.Usage.retrieve()
print(usage.total_usage)
```

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

Exceptions expose `headers`, `request_id`, `retry_after`, `error_type`,
`suggested_action`, `response`, and `to_dict()`. Prefer logging `to_dict()` when
building examples or support-facing error paths.

## Version And Custom HTTP Clients

The SDK exports `mailchannels.__version__` and `mailchannels.get_version()`.
The User-Agent is derived from this value.

For custom transports, implement `mailchannels.SyncHTTPClient` or
`mailchannels.AsyncHTTPClient`. The `request()` method must accept `method`,
`url`, `headers`, optional `json`, optional `params`, and return
`mailchannels.SDKResponse`.

```python
client = mailchannels.Client(
    api_key="YOUR-API-KEY",
    http_client=my_transport,
)
```

Module-level clients can use `mailchannels.default_http_client` and
`mailchannels.default_async_http_client` with any protocol-compatible transport.

## Response Models

The default SDK response remains dict-like and supports attribute access. When
callers set `strict_responses=True` on `Client` or set
`mailchannels.strict_responses = True` for module-level helpers, modeled
endpoints return Pydantic response objects and raise `ResponseValidationError`
when the API response does not match the expected model. When adding a stable
endpoint response, pass its model to `client.request(..., response_model=...)`
and add strict-mode tests.

## Examples

The `examples/` directory has tested examples for async sending, attachments,
suppressions, webhooks, usage, custom HTTP clients, and structured error
handling. Keep examples importable and avoid doing network work at import time;
tests should exercise example functions with fake transports.

## Online Tests

Online tests are marked `online` and require both a real
`MAILCHANNELS_API_KEY` environment variable and the pytest `--online` flag:

```bash
uv run pytest -m online --online
```

The dry-run send test additionally needs `MAILCHANNELS_ONLINE_FROM` and
`MAILCHANNELS_ONLINE_TO`. Optional DKIM listing needs
`MAILCHANNELS_ONLINE_DOMAIN`.

Keep online metrics tests bounded with explicit `start_time` and `end_time`
values. The live `/metrics/volume?interval=day` query can time out when the
range is left implicit.

Do not make online tests deliver messages by default. The real send test must
stay gated behind `MAILCHANNELS_ONLINE_SEND_REAL=1` and should be run directly
when needed:

```bash
uv run pytest tests/test_online_api.py::test_online_send_real_email --online
```

Online tests may mark live MailChannels 5xx responses, timeouts, and transport
failures as `xfail`; 4xx authentication, authorization, validation, or SDK
behavior errors should still fail normally.

Destructive online CRUD tests are marked `online_destructive` and require
`--online`, `--online-destructive`, and `MAILCHANNELS_ONLINE_DESTRUCTIVE=1`.
Keep them manual-only and run them only against a dedicated test account. The
webhook lifecycle test calls `DELETE /webhook`, which removes all configured
webhooks for the account.

## Repository Maintenance

When adding or changing SDK behavior:

- Update tests for the changed behavior.
- Update `README.md` with user-facing documentation.
- Update this `SKILLS.md` when an LLM would need different guidance.
- Update `docs/LEARNINGS.md` for important discoveries or API semantics.
- Run `uv run pytest`, ruff, build, and the SmolVM pytest workflow before
  committing.
- Run `uv run pytest --cov --cov-report=term-missing` when changing tests or
  coverage configuration. The current branch coverage threshold starts at 85%.
- Keep `tests/test_readme_examples.py` aligned with README Python snippets. The
  test should compile every Python fence and execute safe snippets with fake
  transports; skip only examples that need external SDKs or real side effects.
- Run `uv run python scripts/run_consumer_typing.py` after changing public
  exports, type hints, or Pydantic request models.
- Run `uv run python scripts/smoke_wheel_install.py` after `uv build` when
  packaging metadata, dependencies, optional extras, or package data changes.
- Keep `.github/workflows/ci.yml` aligned with the local quality gates when the
  required checks change. Keep online API tests in the manual-only workflow so
  live sends and production API calls require explicit operator intent.
- Keep `.github/workflows/publish.yml` scoped to release publishing. It should
  build and verify distributions before publishing, use the `pypi` GitHub
  environment, and rely on PyPI trusted publishing with `id-token: write`
  instead of long-lived API-token secrets.
- Keep `src/mailchannels/routes.py` updated whenever adding, removing, or
  correcting an API endpoint. Run `uv run python scripts/check_openapi_drift.py`
  when route declarations change; it fails if SDK routes are missing from the
  OpenAPI spec or if the OpenAPI spec has endpoints not declared by the SDK.
- Keep `tests/test_openapi_contract.py` aligned with the route registry so API
  coverage remains visible in the public test tree. The snapshot should match
  `sdk_route_keys()` exactly.
- Keep `tests/test_openapi_request_contract.py` aligned with
  `src/mailchannels/routes.py`. Every SDK route needs an executable contract row
  that calls the public SDK method and validates method, path, JSON/query keys,
  required headers, forbidden headers, and legacy payload keys such as
  `monthly_limit`. Each row also needs an async call so the suite can assert
  sync/async request parity for method, URL, headers, JSON, and query params.
- Keep `tests/test_http_clients.py` covering the real sync and async transport
  wrappers whenever transport signatures or dependency behavior changes.
- Keep `tests/test_errors.py` covering status-to-exception mappings, error
  message extraction, retry metadata, and request ID header variants whenever
  exception behavior changes.
- Prefer Node 24-ready GitHub Actions versions in workflows, such as
  `actions/checkout@v6`, `actions/setup-python@v6`, and
  `astral-sh/setup-uv@v8.1.0` or newer.
- Include `typing_tests` in ruff checks so consumer typing fixtures stay
  formatted with the rest of the repository.
- Keep `setup-uv` workflow caching disabled unless there is a clear need for it;
  this small test matrix runs quickly and parallel cache saves can create noisy
  GitHub Actions annotations.
- When preparing the SmolVM archive on macOS, use `COPYFILE_DISABLE=1` and
  exclude `.venv`, `.git`, `dist`, `.mypy_cache`, `.ruff_cache`, and
  `.pytest_cache` so cache files and extended metadata do not make extraction
  slow or noisy.
