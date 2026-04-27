# MailChannels Python SDK API Reference

This reference is generated from public SDK exports, type hints, Pydantic models, and docstrings in `src/mailchannels`.

For task-oriented examples, start with the README. This file is the formal public surface reference.

- SDK version: `0.1.0`
- Top-level exports: `62`
- Documented public module exports: `175`

## Top-Level Exports

| Name | Kind | Summary |
| --- | --- | --- |
| `ApiError` | `exception` | Raised for MailChannels API failures. |
| `AsyncClientNotConfigured` | `exception` | Raised when async support is requested without an async HTTP client. |
| `AsyncHTTPClient` | `protocol` | Protocol implemented by asynchronous MailChannels HTTP transports. |
| `Attachment` | `Pydantic model` | Email attachment encoded for the MailChannels API. |
| `AuthenticationError` | `exception` | Raised when MailChannels rejects authentication. |
| `BadGatewayError` | `exception` | Raised when MailChannels returns a bad gateway response. |
| `CheckDomain` | `class` | Module-level domain configuration check operations. |
| `CheckDomainParams` | `Pydantic model` | Request body for `/check-domain`. |
| `CheckDomainResource` | `class` | Client-bound domain configuration check operations. |
| `CheckDomainResult` | `Pydantic model` | Domain configuration check response model. |
| `CheckResults` | `Pydantic model` | Grouped check results returned by `/check-domain`. |
| `Client` | `class` | Client for the MailChannels Email API. |
| `ConfigurationError` | `exception` | Raised when SDK configuration is missing or invalid. |
| `ConflictError` | `exception` | Raised when MailChannels reports a resource conflict. |
| `Content` | `Pydantic model` | Email body content part. |
| `Dkim` | `class` | Module-level DKIM key management using global SDK configuration. |
| `DkimResult` | `Pydantic model` | One DKIM result returned by the domain check endpoint. |
| `DkimSetting` | `Pydantic model` | DKIM settings used by the domain check endpoint. |
| `DomainCheckVerdict` | `value` |  |
| `DomainChecks` | `class` | Module-level domain configuration check operations. |
| `EmailAddress` | `Pydantic model` | Email address used for senders and recipients. |
| `EmailHeaders` | `value` |  |
| `EmailParams` | `Pydantic model` | Validated MailChannels email send payload. |
| `Emails` | `class` | Module-level email operations using global SDK configuration. |
| `ForbiddenError` | `exception` | Raised when an account cannot access a requested feature. |
| `HTTPXClient` | `class` | Asynchronous HTTP client backed by httpx. |
| `InvalidRequestError` | `exception` | Raised when MailChannels rejects request parameters or payload shape. |
| `LockdownResult` | `Pydantic model` | Domain Lockdown check result. |
| `MailChannelsError` | `exception` | Base class for MailChannels SDK errors. |
| `Metrics` | `class` | Module-level metrics operations using global SDK configuration. |
| `PayloadTooLargeError` | `exception` | Raised when a request payload exceeds MailChannels limits. |
| `Personalization` | `Pydantic model` | Recipient-specific message customization. |
| `QueuedSendResponse` | `Pydantic model` | Response returned when MailChannels queues an email for async processing. |
| `RateLimitError` | `exception` | Raised when MailChannels asks the caller to slow down. |
| `RequestsClient` | `class` | Synchronous HTTP client backed by requests. |
| `ResponseValidationError` | `exception` | Raised when strict response validation fails. |
| `SDKResponse` | `class` | Normalized HTTP response returned by SDK transports. |
| `SendParams` | `TypedDict` | Resend-style or MailChannels-style email parameters. |
| `SendResponse` | `Pydantic model` | Response returned by MailChannels email send endpoints. |
| `SenderDomainResult` | `Pydantic model` | Sender-domain DNS check result. |
| `ServerError` | `exception` | Raised when MailChannels returns a server-side failure. |
| `SignatureParameters` | `Pydantic model` | Parsed metadata from a MailChannels Signature-Input header. |
| `SpfResult` | `Pydantic model` | SPF check result. |
| `SubAccounts` | `class` | Module-level sub-account operations using global SDK configuration. |
| `Suppressions` | `class` | Module-level suppression list operations. |
| `SyncHTTPClient` | `protocol` | Protocol implemented by synchronous MailChannels HTTP transports. |
| `UNSUBSCRIBE_URL_PLACEHOLDER` | `constant` |  |
| `Usage` | `class` | Module-level parent-account usage operations. |
| `UsageStats` | `Pydantic model` | MailChannels usage statistics for the current billing period. |
| `WebhookEventPayload` | `Pydantic model` | Common fields present on MailChannels delivery event payloads. |
| `Webhooks` | `class` | Module-level webhook operations using global SDK configuration. |
| `__version__` | `constant` |  |
| `api_key` | `value` |  |
| `base_url` | `constant` |  |
| `default_async_http_client` | `value` |  |
| `default_http_client` | `value` |  |
| `get_version` | `function` | Return the installed MailChannels SDK version string. |
| `parse_signature_input` | `function` | Parse a MailChannels RFC 9421 Signature-Input header value. |
| `signature_is_fresh` | `function` | Return whether a signature timestamp is within the allowed age. |
| `signature_key_id` | `function` | Extract the signing key ID from webhook headers. |
| `strict_responses` | `value` |  |
| `verify_content_digest` | `function` | Verify the webhook Content-Digest header against the raw request body. |

## Quick Examples

### Send a dry-run email

```python
mailchannels.Emails.send(
    {
        "from": {"email": "sender@example.com"},
        "to": "recipient@example.net",
        "subject": "Hello",
        "text": "Hello from MailChannels.",
    },
    dry_run=True,
)
```

### Retrieve usage

```python
mailchannels.Usage.retrieve()
```

### List volume metrics

```python
mailchannels.Metrics.volume(interval="day")
```

### List webhooks

```python
mailchannels.Webhooks.list()
```


## Public Modules

### `mailchannels`

Python SDK for the MailChannels Email API.

#### `mailchannels.ApiError`

- Kind: `exception`
- Summary: Raised for MailChannels API failures.

#### `mailchannels.AsyncClientNotConfigured`

- Kind: `exception`
- Summary: Raised when async support is requested without an async HTTP client.

#### `mailchannels.AsyncHTTPClient`

- Kind: `protocol`
- Summary: Protocol implemented by asynchronous MailChannels HTTP transports.
- Signature: `mailchannels.AsyncHTTPClient(*args, **kwargs)`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `request` | `request(method: str, url: str, *, headers: dict[str, str], json: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> SDKResponse` | Send an async HTTP request and return a normalized SDK response. |

#### `mailchannels.Attachment`

- Kind: `Pydantic model`
- Summary: Email attachment encoded for the MailChannels API.
- Signature: `mailchannels.Attachment(content: str, filename: str, type: str | None, disposition: str | None, content_id: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `content` | `str` | yes | `` |
| `filename` | `str` | yes | `` |
| `type` | `str \| None` | no | `None` |
| `disposition` | `str \| None` | no | `None` |
| `content_id` | `str \| None` | no | `None` |

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `from_bytes` | `from_bytes(data: bytes, *, filename: str, content_type: str | None = None, disposition: str = 'attachment', content_id: str | None = None) -> Attachment` | Build an attachment from bytes. |
| `from_file` | `from_file(path: str | Path, *, filename: str | None = None, content_type: str | None = None, disposition: str = 'attachment', content_id: str | None = None) -> Attachment` | Build an attachment from a local file. |
| `from_url` | `from_url(url: str, *, filename: str | None = None, content_type: str | None = None, disposition: str = 'attachment', content_id: str | None = None, timeout: float = 30.0) -> Attachment` | Fetch a remote URL and build an attachment from its bytes. |
| `inline_file` | `inline_file(path: str | Path, *, content_id: str, filename: str | None = None, content_type: str | None = None) -> Attachment` | Build an inline attachment from a local file. |

#### `mailchannels.AuthenticationError`

- Kind: `exception`
- Summary: Raised when MailChannels rejects authentication.

#### `mailchannels.BadGatewayError`

- Kind: `exception`
- Summary: Raised when MailChannels returns a bad gateway response.

#### `mailchannels.CheckDomain`

- Kind: `class`
- Summary: Module-level domain configuration check operations.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `check` | `check(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status. |
| `check_async` | `check_async(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check domain configuration status using async HTTP. |

Example for `check`:

```python
mailchannels.CheckDomain.check("example.com")
```

#### `mailchannels.CheckDomainParams`

- Kind: `Pydantic model`
- Summary: Request body for `/check-domain`.
- Signature: `mailchannels.CheckDomainParams(domain: str, sender_id: str | None, dkim_settings: list[mailchannels.domain_checks.DkimSetting | dict[str, str]] | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `domain` | `str` | yes | `` |
| `sender_id` | `str \| None` | no | `None` |
| `dkim_settings` | `list[mailchannels.domain_checks.DkimSetting \| dict[str, str]] \| None` | no | `None` |

#### `mailchannels.CheckDomainResource`

- Kind: `class`
- Summary: Client-bound domain configuration check operations.
- Signature: `mailchannels.CheckDomainResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `check` | `check(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status. |
| `check_async` | `check_async(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check domain configuration status using async HTTP. |

#### `mailchannels.CheckDomainResult`

- Kind: `Pydantic model`
- Summary: Domain configuration check response model.
- Signature: `mailchannels.CheckDomainResult(check_results: mailchannels.domain_checks.CheckResults | None, references: list[str] | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `check_results` | `mailchannels.domain_checks.CheckResults \| None` | no | `None` |
| `references` | `list[str] \| None` | no | `None` |

#### `mailchannels.CheckResults`

- Kind: `Pydantic model`
- Summary: Grouped check results returned by `/check-domain`.
- Signature: `mailchannels.CheckResults(dkim: list[mailchannels.domain_checks.DkimResult] | None, domain_lockdown: mailchannels.domain_checks.LockdownResult | None, sender_domain: mailchannels.domain_checks.SenderDomainResult | None, spf: mailchannels.domain_checks.SpfResult | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `dkim` | `list[mailchannels.domain_checks.DkimResult] \| None` | no | `None` |
| `domain_lockdown` | `mailchannels.domain_checks.LockdownResult \| None` | no | `None` |
| `sender_domain` | `mailchannels.domain_checks.SenderDomainResult \| None` | no | `None` |
| `spf` | `mailchannels.domain_checks.SpfResult \| None` | no | `None` |

#### `mailchannels.Client`

- Kind: `class`
- Summary: Client for the MailChannels Email API.
- Signature: `mailchannels.Client(*, api_key: str | None = None, base_url: str | None = None, http_client: SyncHTTPClient | None = None, async_http_client: AsyncHTTPClient | None = None, strict_responses: bool = False) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `request` | `request(method: str, path: str, *, json: dict[str, Any] | None = None, params: dict[str, Any] | None = None, extra_headers: dict[str, str] | None = None, require_api_key: bool = True, response_model: type[ResponseModel] | None = None) -> Any` | Send a synchronous API request. |
| `request_async` | `request_async(method: str, path: str, *, json: dict[str, Any] | None = None, params: dict[str, Any] | None = None, extra_headers: dict[str, str] | None = None, require_api_key: bool = True, response_model: type[ResponseModel] | None = None) -> Any` | Send an asynchronous API request. |

#### `mailchannels.ConfigurationError`

- Kind: `exception`
- Summary: Raised when SDK configuration is missing or invalid.

#### `mailchannels.ConflictError`

- Kind: `exception`
- Summary: Raised when MailChannels reports a resource conflict.

#### `mailchannels.Content`

- Kind: `Pydantic model`
- Summary: Email body content part.
- Signature: `mailchannels.Content(type: Union, value: str, template_type: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `type` | `Union` | yes | `` |
| `value` | `str` | yes | `` |
| `template_type` | `Optional` | no | `None` |

#### `mailchannels.Dkim`

- Kind: `class`
- Summary: Module-level DKIM key management using global SDK configuration.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `create` | `create(domain: str, *, selector: str, algorithm: DkimAlgorithm | None = None, key_length: int | None = None) -> dict[str, Any]` | Create a MailChannels-hosted DKIM key pair for a domain. |
| `create_async` | `create_async(domain: str, *, selector: str, algorithm: DkimAlgorithm | None = None, key_length: int | None = None) -> dict[str, Any]` | Create a MailChannels-hosted DKIM key pair using async HTTP. |
| `list` | `list(domain: str, *, selector: str | None = None, status: DkimKeyStatus | None = None, offset: int | None = None, limit: int | None = None, include_dns_record: bool | None = None) -> dict[str, Any]` | Retrieve MailChannels-hosted DKIM keys for a domain. |
| `list_async` | `list_async(domain: str, *, selector: str | None = None, status: DkimKeyStatus | None = None, offset: int | None = None, limit: int | None = None, include_dns_record: bool | None = None) -> dict[str, Any]` | Retrieve MailChannels-hosted DKIM keys using async HTTP. |
| `rotate` | `rotate(domain: str, selector: str, *, new_selector: str) -> dict[str, Any]` | Rotate a MailChannels-hosted DKIM key pair. |
| `rotate_async` | `rotate_async(domain: str, selector: str, *, new_selector: str) -> dict[str, Any]` | Rotate a MailChannels-hosted DKIM key pair using async HTTP. |
| `update_status` | `update_status(domain: str, selector: str, *, status: DkimUpdateStatus) -> dict[str, Any]` | Update the status of a MailChannels-hosted DKIM key pair. |
| `update_status_async` | `update_status_async(domain: str, selector: str, *, status: DkimUpdateStatus) -> dict[str, Any]` | Update the status of a MailChannels-hosted DKIM key pair using async HTTP. |

Example for `create`:

```python
mailchannels.Dkim.create("example.com", selector="mcdkim")
```

#### `mailchannels.DkimResult`

- Kind: `Pydantic model`
- Summary: One DKIM result returned by the domain check endpoint.
- Signature: `mailchannels.DkimResult(dkim_domain: str | None, dkim_selector: str | None, dkim_key_status: str | None, reason: str | None, verdict: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `dkim_domain` | `str \| None` | no | `None` |
| `dkim_selector` | `str \| None` | no | `None` |
| `dkim_key_status` | `str \| None` | no | `None` |
| `reason` | `str \| None` | no | `None` |
| `verdict` | `Optional` | no | `None` |

#### `mailchannels.DkimSetting`

- Kind: `Pydantic model`
- Summary: DKIM settings used by the domain check endpoint.
- Signature: `mailchannels.DkimSetting(dkim_domain: str | None, dkim_selector: str | None, dkim_private_key: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `dkim_domain` | `str \| None` | no | `None` |
| `dkim_selector` | `str \| None` | no | `None` |
| `dkim_private_key` | `str \| None` | no | `None` |

#### `mailchannels.DomainCheckVerdict`

- Kind: `value`
- Summary: 

#### `mailchannels.DomainChecks`

- Kind: `class`
- Summary: Module-level domain configuration check operations.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `check` | `check(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status. |
| `check_async` | `check_async(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check domain configuration status using async HTTP. |

#### `mailchannels.EmailAddress`

- Kind: `Pydantic model`
- Summary: Email address used for senders and recipients.
- Signature: `mailchannels.EmailAddress(email: str, name: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `email` | `str` | yes | `` |
| `name` | `str \| None` | no | `None` |

#### `mailchannels.EmailHeaders`

- Kind: `value`
- Summary: 

#### `mailchannels.EmailParams`

- Kind: `Pydantic model`
- Summary: Validated MailChannels email send payload.
- Signature: `mailchannels.EmailParams(personalizations: list, from: EmailAddress, subject: str, content: list, reply_to: mailchannels.emails.EmailAddress | None, headers: dict[str, str] | None, attachments: list[mailchannels.emails.Attachment] | None, transactional: bool | None, dkim_domain: str | None, dkim_private_key: str | None, dkim_selector: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `personalizations` | `list` | yes | `` |
| `from_` | `EmailAddress` | yes | `` |
| `subject` | `str` | yes | `` |
| `content` | `list` | yes | `` |
| `reply_to` | `mailchannels.emails.EmailAddress \| None` | no | `None` |
| `headers` | `dict[str, str] \| None` | no | `None` |
| `attachments` | `list[mailchannels.emails.Attachment] \| None` | no | `None` |
| `transactional` | `bool \| None` | no | `None` |
| `dkim_domain` | `str \| None` | no | `None` |
| `dkim_private_key` | `str \| None` | no | `None` |
| `dkim_selector` | `str \| None` | no | `None` |

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `to_payload` | `to_payload() -> dict[str, Any]` | Convert this email model to a MailChannels API payload. |

#### `mailchannels.Emails`

- Kind: `class`
- Summary: Module-level email operations using global SDK configuration.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `queue` | `queue(params: SendParamsType | EmailParams) -> dict[str, Any]` | Queue an email through the globally configured client. |
| `queue_async` | `queue_async(params: SendParamsType | EmailParams) -> dict[str, Any]` | Queue an email through the globally configured async client. |
| `send` | `send(params: SendParamsType | EmailParams, *, dry_run: bool = False) -> dict[str, Any]` | Send an email through the globally configured client. |
| `send_async` | `send_async(params: SendParamsType | EmailParams, *, dry_run: bool = False) -> dict[str, Any]` | Send an email through the globally configured async client. |

Example for `queue`:

```python
mailchannels.Emails.queue({"from": {"email": "sender@example.com"}, "to": "recipient@example.net", "subject": "Queued", "text": "Hello"})
```

Example for `send`:

```python
mailchannels.Emails.send({"from": {"email": "sender@example.com"}, "to": "recipient@example.net", "subject": "Hello", "text": "Hello"})
```

#### `mailchannels.ForbiddenError`

- Kind: `exception`
- Summary: Raised when an account cannot access a requested feature.

#### `mailchannels.HTTPXClient`

- Kind: `class`
- Summary: Asynchronous HTTP client backed by httpx.
- Signature: `mailchannels.HTTPXClient(*, timeout: float = 30.0) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `request` | `request(method: str, url: str, *, headers: dict[str, str], json: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> SDKResponse` | Send an async HTTP request and return a normalized SDK response. |

#### `mailchannels.InvalidRequestError`

- Kind: `exception`
- Summary: Raised when MailChannels rejects request parameters or payload shape.

#### `mailchannels.LockdownResult`

- Kind: `Pydantic model`
- Summary: Domain Lockdown check result.
- Signature: `mailchannels.LockdownResult(reason: str | None, verdict: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `reason` | `str \| None` | no | `None` |
| `verdict` | `Optional` | no | `None` |

#### `mailchannels.MailChannelsError`

- Kind: `exception`
- Summary: Base class for MailChannels SDK errors.
- Signature: `mailchannels.MailChannelsError(message: str, *, status_code: int | None = None, code: str | None = None, response: Any | None = None, headers: dict[str, str] | None = None, error_type: str | None = None, request_id: str | None = None, suggested_action: str | None = None) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `to_dict` | `to_dict() -> dict[str, Any]` | Return structured metadata for logging or diagnostics. |

#### `mailchannels.Metrics`

- Kind: `class`
- Summary: Module-level metrics operations using global SDK configuration.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `engagement` | `engagement(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve engagement metrics. |
| `engagement_async` | `engagement_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve engagement metrics using async HTTP. |
| `performance` | `performance(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve performance metrics. |
| `performance_async` | `performance_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve performance metrics using async HTTP. |
| `recipient_behavior` | `recipient_behavior(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve recipient behaviour metrics using US spelling. |
| `recipient_behavior_async` | `recipient_behavior_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve recipient behaviour metrics using US spelling and async HTTP. |
| `recipient_behaviour` | `recipient_behaviour(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve recipient behaviour metrics. |
| `recipient_behaviour_async` | `recipient_behaviour_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve recipient behaviour metrics using async HTTP. |
| `senders` | `senders(sender_type: MetricsSenderType, *, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, limit: int | None = None, offset: int | None = None, sort_order: MetricsSortOrder | None = None) -> dict[str, Any]` | Retrieve sender metrics grouped by campaigns or sub-accounts. |
| `senders_async` | `senders_async(sender_type: MetricsSenderType, *, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, limit: int | None = None, offset: int | None = None, sort_order: MetricsSortOrder | None = None) -> dict[str, Any]` | Retrieve sender metrics using async HTTP. |
| `volume` | `volume(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve volume metrics. |
| `volume_async` | `volume_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve volume metrics using async HTTP. |

Example for `volume`:

```python
mailchannels.Metrics.volume(start_time="2026-04-01", interval="day")
```

#### `mailchannels.PayloadTooLargeError`

- Kind: `exception`
- Summary: Raised when a request payload exceeds MailChannels limits.

#### `mailchannels.Personalization`

- Kind: `Pydantic model`
- Summary: Recipient-specific message customization.
- Signature: `mailchannels.Personalization(to: list, cc: list[mailchannels.emails.EmailAddress] | None, bcc: list[mailchannels.emails.EmailAddress] | None, subject: str | None, from: mailchannels.emails.EmailAddress | None, reply_to: mailchannels.emails.EmailAddress | None, headers: dict[str, str] | None, substitutions: dict[str, str] | None, dynamic_template_data: dict[str, Any] | None, dkim_domain: str | None, dkim_private_key: str | None, dkim_selector: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `to` | `list` | no | `` |
| `cc` | `list[mailchannels.emails.EmailAddress] \| None` | no | `None` |
| `bcc` | `list[mailchannels.emails.EmailAddress] \| None` | no | `None` |
| `subject` | `str \| None` | no | `None` |
| `from_` | `mailchannels.emails.EmailAddress \| None` | no | `None` |
| `reply_to` | `mailchannels.emails.EmailAddress \| None` | no | `None` |
| `headers` | `dict[str, str] \| None` | no | `None` |
| `substitutions` | `dict[str, str] \| None` | no | `None` |
| `dynamic_template_data` | `dict[str, Any] \| None` | no | `None` |
| `dkim_domain` | `str \| None` | no | `None` |
| `dkim_private_key` | `str \| None` | no | `None` |
| `dkim_selector` | `str \| None` | no | `None` |

#### `mailchannels.QueuedSendResponse`

- Kind: `Pydantic model`
- Summary: Response returned when MailChannels queues an email for async processing.
- Signature: `mailchannels.QueuedSendResponse()`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |

#### `mailchannels.RateLimitError`

- Kind: `exception`
- Summary: Raised when MailChannels asks the caller to slow down.

#### `mailchannels.RequestsClient`

- Kind: `class`
- Summary: Synchronous HTTP client backed by requests.
- Signature: `mailchannels.RequestsClient(*, timeout: float = 30.0) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `request` | `request(method: str, url: str, *, headers: dict[str, str], json: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> SDKResponse` | Send an HTTP request and return a normalized SDK response. |

#### `mailchannels.ResponseValidationError`

- Kind: `exception`
- Summary: Raised when strict response validation fails.

#### `mailchannels.SDKResponse`

- Kind: `class`
- Summary: Normalized HTTP response returned by SDK transports.
- Signature: `mailchannels.SDKResponse(status_code: int, data: Any, text: str, headers: dict[str, str] | None = None) -> None`

#### `mailchannels.SendParams`

- Kind: `TypedDict`
- Summary: Resend-style or MailChannels-style email parameters.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `attachments` | `list` | no |
| `bcc` | `list[mailchannels.emails.EmailAddressDict] \| mailchannels.emails.EmailAddressDict \| list[str] \| str` | no |
| `cc` | `list[mailchannels.emails.EmailAddressDict] \| mailchannels.emails.EmailAddressDict \| list[str] \| str` | no |
| `content` | `list` | no |
| `dkim_domain` | `str` | no |
| `dkim_private_key` | `str` | no |
| `dkim_selector` | `str` | no |
| `from_` | `EmailAddressDict` | no |
| `from_address` | `EmailAddressDict` | no |
| `from_display_name` | `str` | no |
| `from_email` | `EmailAddressDict` | no |
| `from_field` | `EmailAddressDict` | no |
| `from_name` | `str` | no |
| `headers` | `dict` | no |
| `html` | `str` | no |
| `personalizations` | `list` | no |
| `reply_to` | `mailchannels.emails.EmailAddressDict \| str` | no |
| `subject` | `str` | no |
| `text` | `str` | no |
| `to` | `list[mailchannels.emails.EmailAddressDict] \| mailchannels.emails.EmailAddressDict \| list[str] \| str` | no |
| `transactional` | `bool` | no |

#### `mailchannels.SendResponse`

- Kind: `Pydantic model`
- Summary: Response returned by MailChannels email send endpoints.
- Signature: `mailchannels.SendResponse()`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |

#### `mailchannels.SenderDomainResult`

- Kind: `Pydantic model`
- Summary: Sender-domain DNS check result.
- Signature: `mailchannels.SenderDomainResult(a: mailchannels.domain_checks.SenderDomainRecordResult | None, mx: mailchannels.domain_checks.SenderDomainRecordResult | None, verdict: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `a` | `mailchannels.domain_checks.SenderDomainRecordResult \| None` | no | `None` |
| `mx` | `mailchannels.domain_checks.SenderDomainRecordResult \| None` | no | `None` |
| `verdict` | `Optional` | no | `None` |

#### `mailchannels.ServerError`

- Kind: `exception`
- Summary: Raised when MailChannels returns a server-side failure.

#### `mailchannels.SignatureParameters`

- Kind: `Pydantic model`
- Summary: Parsed metadata from a MailChannels Signature-Input header.
- Signature: `mailchannels.SignatureParameters(signature_name: str, covered_components: list, created: int | None, algorithm: str | None, key_id: str | None, raw: str)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `signature_name` | `str` | yes | `` |
| `covered_components` | `list` | yes | `` |
| `created` | `int \| None` | no | `None` |
| `algorithm` | `str \| None` | no | `None` |
| `key_id` | `str \| None` | no | `None` |
| `raw` | `str` | yes | `` |

#### `mailchannels.SpfResult`

- Kind: `Pydantic model`
- Summary: SPF check result.
- Signature: `mailchannels.SpfResult(reason: str | None, spfRecord: str | None, spfRecordError: str | None, verdict: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `reason` | `str \| None` | no | `None` |
| `spfRecord` | `str \| None` | no | `None` |
| `spfRecordError` | `str \| None` | no | `None` |
| `verdict` | `Optional` | no | `None` |

#### `mailchannels.SubAccounts`

- Kind: `class`
- Summary: Module-level sub-account operations using global SDK configuration.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `activate` | `activate(handle: str) -> dict[str, Any]` | Activate a suspended sub-account. |
| `activate_async` | `activate_async(handle: str) -> dict[str, Any]` | Activate a suspended sub-account using async HTTP. |
| `create` | `create(*, company_name: str | None = None, handle: str | None = None) -> dict[str, Any]` | Create a sub-account under the parent account. |
| `create_async` | `create_async(*, company_name: str | None = None, handle: str | None = None) -> dict[str, Any]` | Create a sub-account under the parent account using async HTTP. |
| `delete` | `delete(handle: str) -> dict[str, Any]` | Delete a sub-account. |
| `delete_async` | `delete_async(handle: str) -> dict[str, Any]` | Delete a sub-account using async HTTP. |
| `list` | `list(*, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve sub-accounts for the parent account. |
| `list_async` | `list_async(*, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve sub-accounts for the parent account using async HTTP. |
| `retrieve_usage` | `retrieve_usage(handle: str) -> dict[str, Any]` | Retrieve usage statistics for a sub-account. |
| `retrieve_usage_async` | `retrieve_usage_async(handle: str) -> dict[str, Any]` | Retrieve usage statistics for a sub-account using async HTTP. |
| `suspend` | `suspend(handle: str) -> dict[str, Any]` | Suspend a sub-account. |
| `suspend_async` | `suspend_async(handle: str) -> dict[str, Any]` | Suspend a sub-account using async HTTP. |

Example for `create`:

```python
mailchannels.SubAccounts.create(company_name="Client A", handle="clienta")
```

#### `mailchannels.Suppressions`

- Kind: `class`
- Summary: Module-level suppression list operations.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `create` | `create(entries: list_type[SuppressionEntryParams], *, add_to_sub_accounts: bool | None = None) -> dict[str, Any]` | Create suppression entries. |
| `create_async` | `create_async(entries: list_type[SuppressionEntryParams], *, add_to_sub_accounts: bool | None = None) -> dict[str, Any]` | Create suppression entries using async HTTP. |
| `delete` | `delete(recipient: str, *, source: SuppressionDeleteSource | None = None) -> dict[str, Any]` | Delete suppression entries for a recipient. |
| `delete_async` | `delete_async(recipient: str, *, source: SuppressionDeleteSource | None = None) -> dict[str, Any]` | Delete suppression entries for a recipient using async HTTP. |
| `list` | `list(**kwargs: Any) -> dict[str, Any]` | Retrieve suppression entries. |
| `list_async` | `list_async(**kwargs: Any) -> dict[str, Any]` | Retrieve suppression entries using async HTTP. |

Example for `list`:

```python
mailchannels.Suppressions.list(source="api", limit=100)
```

#### `mailchannels.SyncHTTPClient`

- Kind: `protocol`
- Summary: Protocol implemented by synchronous MailChannels HTTP transports.
- Signature: `mailchannels.SyncHTTPClient(*args, **kwargs)`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `request` | `request(method: str, url: str, *, headers: dict[str, str], json: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> SDKResponse` | Send an HTTP request and return a normalized SDK response. |

#### `mailchannels.UNSUBSCRIBE_URL_PLACEHOLDER`

- Kind: `constant`
- Summary: 

#### `mailchannels.Usage`

- Kind: `class`
- Summary: Module-level parent-account usage operations.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `retrieve` | `retrieve() -> dict[str, Any]` | Retrieve parent-account usage for the current billing period. |
| `retrieve_async` | `retrieve_async() -> dict[str, Any]` | Retrieve parent-account usage using async HTTP. |

Example for `retrieve`:

```python
mailchannels.Usage.retrieve()
```

#### `mailchannels.UsageStats`

- Kind: `Pydantic model`
- Summary: MailChannels usage statistics for the current billing period.
- Signature: `mailchannels.UsageStats(total_usage: int, period_start_date: str | None, period_end_date: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `total_usage` | `int` | yes | `` |
| `period_start_date` | `str \| None` | no | `None` |
| `period_end_date` | `str \| None` | no | `None` |

#### `mailchannels.WebhookEventPayload`

- Kind: `Pydantic model`
- Summary: Common fields present on MailChannels delivery event payloads.
- Signature: `mailchannels.WebhookEventPayload(email: str | None, customer_handle: str, timestamp: int, event: Union, request_id: str | None, smtp_id: str | None, recipients: list[str] | None, status: str | None, reason: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `email` | `str \| None` | no | `None` |
| `customer_handle` | `str` | yes | `` |
| `timestamp` | `int` | yes | `` |
| `event` | `Union` | yes | `` |
| `request_id` | `str \| None` | no | `None` |
| `smtp_id` | `str \| None` | no | `None` |
| `recipients` | `list[str] \| None` | no | `None` |
| `status` | `str \| None` | no | `None` |
| `reason` | `str \| None` | no | `None` |

#### `mailchannels.Webhooks`

- Kind: `class`
- Summary: Module-level webhook operations using global SDK configuration.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `batches` | `batches(*, created_after: str | None = None, created_before: str | None = None, statuses: list_type[WebhookBatchStatus] | None = None, webhook: str | None = None, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve webhook delivery batches. |
| `batches_async` | `batches_async(*, created_after: str | None = None, created_before: str | None = None, statuses: list_type[WebhookBatchStatus] | None = None, webhook: str | None = None, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve webhook delivery batches using async HTTP. |
| `create` | `create(endpoint: str) -> dict[str, Any]` | Enroll a webhook endpoint for delivery events. |
| `create_async` | `create_async(endpoint: str) -> dict[str, Any]` | Enroll a webhook endpoint for delivery events using async HTTP. |
| `delete` | `delete() -> dict[str, Any]` | Delete all configured webhook endpoints. |
| `delete_async` | `delete_async() -> dict[str, Any]` | Delete all configured webhook endpoints using async HTTP. |
| `list` | `list() -> dict[str, Any]` | Retrieve configured webhook endpoints. |
| `list_async` | `list_async() -> dict[str, Any]` | Retrieve configured webhook endpoints using async HTTP. |
| `parse_signature_input` | `parse_signature_input(value: str) -> SignatureParameters` | Parse a MailChannels RFC 9421 Signature-Input header value. |
| `public_key` | `public_key(key_id: str) -> dict[str, Any]` | Retrieve a webhook public signing key by ID. |
| `public_key_async` | `public_key_async(key_id: str) -> dict[str, Any]` | Retrieve a webhook public signing key by ID using async HTTP. |
| `resend_batch` | `resend_batch(batch_id: int, *, customer_handle: str) -> dict[str, Any]` | Synchronously resend one webhook batch. |
| `resend_batch_async` | `resend_batch_async(batch_id: int, *, customer_handle: str) -> dict[str, Any]` | Synchronously resend one webhook batch using async HTTP. |
| `signature_is_fresh` | `signature_is_fresh(parameters: SignatureParameters, *, tolerance_seconds: int = 300, now: int | None = None) -> bool` | Return whether a signature timestamp is within the allowed age. |
| `signature_key_id` | `signature_key_id(headers: dict[str, str]) -> str | None` | Extract the signing key ID from webhook headers. |
| `validate` | `validate(*, request_id: str | None = None) -> dict[str, Any]` | Validate enrolled webhook endpoints with a test event. |
| `validate_async` | `validate_async(*, request_id: str | None = None) -> dict[str, Any]` | Validate enrolled webhook endpoints with a test event using async HTTP. |
| `verify_content_digest` | `verify_content_digest(headers: dict[str, str], body: bytes | str) -> bool` | Verify the webhook Content-Digest header against the raw body. |

Example for `list`:

```python
mailchannels.Webhooks.list()
```

#### `mailchannels.__version__`

- Kind: `constant`
- Summary: 

#### `mailchannels.api_key`

- Kind: `value`
- Summary: 

#### `mailchannels.base_url`

- Kind: `constant`
- Summary: 

#### `mailchannels.default_async_http_client`

- Kind: `value`
- Summary: 

#### `mailchannels.default_http_client`

- Kind: `value`
- Summary: 

#### `mailchannels.get_version`

- Kind: `function`
- Summary: Return the installed MailChannels SDK version string.
- Signature: `mailchannels.get_version() -> str`

#### `mailchannels.parse_signature_input`

- Kind: `function`
- Summary: Parse a MailChannels RFC 9421 Signature-Input header value.
- Signature: `mailchannels.parse_signature_input(value: str) -> SignatureParameters`

#### `mailchannels.signature_is_fresh`

- Kind: `function`
- Summary: Return whether a signature timestamp is within the allowed age.
- Signature: `mailchannels.signature_is_fresh(parameters: SignatureParameters, *, tolerance_seconds: int = 300, now: int | None = None) -> bool`

#### `mailchannels.signature_key_id`

- Kind: `function`
- Summary: Extract the signing key ID from webhook headers.
- Signature: `mailchannels.signature_key_id(headers: dict[str, str]) -> str | None`

#### `mailchannels.strict_responses`

- Kind: `value`
- Summary: 

#### `mailchannels.verify_content_digest`

- Kind: `function`
- Summary: Verify the webhook Content-Digest header against the raw request body.
- Signature: `mailchannels.verify_content_digest(headers: dict[str, str], body: bytes | str) -> bool`

### `mailchannels.emails`

Email resource exports.

#### `mailchannels.emails.Attachment`

- Kind: `Pydantic model`
- Summary: Email attachment encoded for the MailChannels API.
- Signature: `mailchannels.emails.Attachment(content: str, filename: str, type: str | None, disposition: str | None, content_id: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `content` | `str` | yes | `` |
| `filename` | `str` | yes | `` |
| `type` | `str \| None` | no | `None` |
| `disposition` | `str \| None` | no | `None` |
| `content_id` | `str \| None` | no | `None` |

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `from_bytes` | `from_bytes(data: bytes, *, filename: str, content_type: str | None = None, disposition: str = 'attachment', content_id: str | None = None) -> Attachment` | Build an attachment from bytes. |
| `from_file` | `from_file(path: str | Path, *, filename: str | None = None, content_type: str | None = None, disposition: str = 'attachment', content_id: str | None = None) -> Attachment` | Build an attachment from a local file. |
| `from_url` | `from_url(url: str, *, filename: str | None = None, content_type: str | None = None, disposition: str = 'attachment', content_id: str | None = None, timeout: float = 30.0) -> Attachment` | Fetch a remote URL and build an attachment from its bytes. |
| `inline_file` | `inline_file(path: str | Path, *, content_id: str, filename: str | None = None, content_type: str | None = None) -> Attachment` | Build an inline attachment from a local file. |

#### `mailchannels.emails.AttachmentDict`

- Kind: `TypedDict`
- Summary: Dictionary form of a MailChannels attachment.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `content` | `str` | no |
| `content_id` | `str` | no |
| `disposition` | `str` | no |
| `filename` | `str` | no |
| `type` | `str` | no |

#### `mailchannels.emails.Content`

- Kind: `Pydantic model`
- Summary: Email body content part.
- Signature: `mailchannels.emails.Content(type: Union, value: str, template_type: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `type` | `Union` | yes | `` |
| `value` | `str` | yes | `` |
| `template_type` | `Optional` | no | `None` |

#### `mailchannels.emails.ContentDict`

- Kind: `TypedDict`
- Summary: Dictionary form of a MailChannels content part.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `template_type` | `Literal` | no |
| `type` | `str` | no |
| `value` | `str` | no |

#### `mailchannels.emails.EmailAddress`

- Kind: `Pydantic model`
- Summary: Email address used for senders and recipients.
- Signature: `mailchannels.emails.EmailAddress(email: str, name: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `email` | `str` | yes | `` |
| `name` | `str \| None` | no | `None` |

#### `mailchannels.emails.EmailAddressDict`

- Kind: `TypedDict`
- Summary: Dictionary form of a MailChannels email address.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `email` | `str` | no |
| `name` | `str` | no |

#### `mailchannels.emails.EmailHeaders`

- Kind: `value`
- Summary: 

#### `mailchannels.emails.EmailParams`

- Kind: `Pydantic model`
- Summary: Validated MailChannels email send payload.
- Signature: `mailchannels.emails.EmailParams(personalizations: list, from: EmailAddress, subject: str, content: list, reply_to: mailchannels.emails.EmailAddress | None, headers: dict[str, str] | None, attachments: list[mailchannels.emails.Attachment] | None, transactional: bool | None, dkim_domain: str | None, dkim_private_key: str | None, dkim_selector: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `personalizations` | `list` | yes | `` |
| `from_` | `EmailAddress` | yes | `` |
| `subject` | `str` | yes | `` |
| `content` | `list` | yes | `` |
| `reply_to` | `mailchannels.emails.EmailAddress \| None` | no | `None` |
| `headers` | `dict[str, str] \| None` | no | `None` |
| `attachments` | `list[mailchannels.emails.Attachment] \| None` | no | `None` |
| `transactional` | `bool \| None` | no | `None` |
| `dkim_domain` | `str \| None` | no | `None` |
| `dkim_private_key` | `str \| None` | no | `None` |
| `dkim_selector` | `str \| None` | no | `None` |

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `to_payload` | `to_payload() -> dict[str, Any]` | Convert this email model to a MailChannels API payload. |

#### `mailchannels.emails.Emails`

- Kind: `class`
- Summary: Module-level email operations using global SDK configuration.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `queue` | `queue(params: SendParamsType | EmailParams) -> dict[str, Any]` | Queue an email through the globally configured client. |
| `queue_async` | `queue_async(params: SendParamsType | EmailParams) -> dict[str, Any]` | Queue an email through the globally configured async client. |
| `send` | `send(params: SendParamsType | EmailParams, *, dry_run: bool = False) -> dict[str, Any]` | Send an email through the globally configured client. |
| `send_async` | `send_async(params: SendParamsType | EmailParams, *, dry_run: bool = False) -> dict[str, Any]` | Send an email through the globally configured async client. |

#### `mailchannels.emails.EmailsResource`

- Kind: `class`
- Summary: Client-bound email operations.
- Signature: `mailchannels.emails.EmailsResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `queue` | `queue(params: SendParamsType | EmailParams) -> dict[str, Any]` | Queue an email through the MailChannels `/send-async` endpoint. |
| `queue_async` | `queue_async(params: SendParamsType | EmailParams) -> dict[str, Any]` | Queue an email through `/send-async` using async HTTP. |
| `send` | `send(params: SendParamsType | EmailParams, *, dry_run: bool = False) -> dict[str, Any]` | Send an email through the MailChannels `/send` endpoint. |
| `send_async` | `send_async(params: SendParamsType | EmailParams, *, dry_run: bool = False) -> dict[str, Any]` | Send an email through `/send` using async HTTP. |

#### `mailchannels.emails.Personalization`

- Kind: `Pydantic model`
- Summary: Recipient-specific message customization.
- Signature: `mailchannels.emails.Personalization(to: list, cc: list[mailchannels.emails.EmailAddress] | None, bcc: list[mailchannels.emails.EmailAddress] | None, subject: str | None, from: mailchannels.emails.EmailAddress | None, reply_to: mailchannels.emails.EmailAddress | None, headers: dict[str, str] | None, substitutions: dict[str, str] | None, dynamic_template_data: dict[str, Any] | None, dkim_domain: str | None, dkim_private_key: str | None, dkim_selector: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `to` | `list` | no | `` |
| `cc` | `list[mailchannels.emails.EmailAddress] \| None` | no | `None` |
| `bcc` | `list[mailchannels.emails.EmailAddress] \| None` | no | `None` |
| `subject` | `str \| None` | no | `None` |
| `from_` | `mailchannels.emails.EmailAddress \| None` | no | `None` |
| `reply_to` | `mailchannels.emails.EmailAddress \| None` | no | `None` |
| `headers` | `dict[str, str] \| None` | no | `None` |
| `substitutions` | `dict[str, str] \| None` | no | `None` |
| `dynamic_template_data` | `dict[str, Any] \| None` | no | `None` |
| `dkim_domain` | `str \| None` | no | `None` |
| `dkim_private_key` | `str \| None` | no | `None` |
| `dkim_selector` | `str \| None` | no | `None` |

#### `mailchannels.emails.PersonalizationDict`

- Kind: `TypedDict`
- Summary: Dictionary form of a MailChannels personalization.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `bcc` | `list` | no |
| `cc` | `list` | no |
| `dkim_domain` | `str` | no |
| `dkim_private_key` | `str` | no |
| `dkim_selector` | `str` | no |
| `dynamic_template_data` | `dict` | no |
| `from_` | `EmailAddressDict` | no |
| `headers` | `dict` | no |
| `reply_to` | `EmailAddressDict` | no |
| `subject` | `str` | no |
| `substitutions` | `dict` | no |
| `to` | `list` | no |

#### `mailchannels.emails.QueuedSendResponse`

- Kind: `Pydantic model`
- Summary: Response returned when MailChannels queues an email for async processing.
- Signature: `mailchannels.emails.QueuedSendResponse()`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |

#### `mailchannels.emails.SendParams`

- Kind: `TypedDict`
- Summary: Resend-style or MailChannels-style email parameters.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `attachments` | `list` | no |
| `bcc` | `list[mailchannels.emails.EmailAddressDict] \| mailchannels.emails.EmailAddressDict \| list[str] \| str` | no |
| `cc` | `list[mailchannels.emails.EmailAddressDict] \| mailchannels.emails.EmailAddressDict \| list[str] \| str` | no |
| `content` | `list` | no |
| `dkim_domain` | `str` | no |
| `dkim_private_key` | `str` | no |
| `dkim_selector` | `str` | no |
| `from_` | `EmailAddressDict` | no |
| `from_address` | `EmailAddressDict` | no |
| `from_display_name` | `str` | no |
| `from_email` | `EmailAddressDict` | no |
| `from_field` | `EmailAddressDict` | no |
| `from_name` | `str` | no |
| `headers` | `dict` | no |
| `html` | `str` | no |
| `personalizations` | `list` | no |
| `reply_to` | `mailchannels.emails.EmailAddressDict \| str` | no |
| `subject` | `str` | no |
| `text` | `str` | no |
| `to` | `list[mailchannels.emails.EmailAddressDict] \| mailchannels.emails.EmailAddressDict \| list[str] \| str` | no |
| `transactional` | `bool` | no |

#### `mailchannels.emails.SendResponse`

- Kind: `Pydantic model`
- Summary: Response returned by MailChannels email send endpoints.
- Signature: `mailchannels.emails.SendResponse()`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |

#### `mailchannels.emails.UNSUBSCRIBE_URL_PLACEHOLDER`

- Kind: `constant`
- Summary: 

#### `mailchannels.emails.normalize_email_params`

- Kind: `function`
- Summary: Normalize SDK email parameters into MailChannels API JSON.
- Signature: `mailchannels.emails.normalize_email_params(params: SendParamsType | EmailParams) -> dict[str, Any]`

### `mailchannels.domain_checks`

Domain-check resource exports.

#### `mailchannels.domain_checks.CheckDomain`

- Kind: `class`
- Summary: Module-level domain configuration check operations.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `check` | `check(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status. |
| `check_async` | `check_async(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check domain configuration status using async HTTP. |

#### `mailchannels.domain_checks.CheckDomainParams`

- Kind: `Pydantic model`
- Summary: Request body for `/check-domain`.
- Signature: `mailchannels.domain_checks.CheckDomainParams(domain: str, sender_id: str | None, dkim_settings: list[mailchannels.domain_checks.DkimSetting | dict[str, str]] | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `domain` | `str` | yes | `` |
| `sender_id` | `str \| None` | no | `None` |
| `dkim_settings` | `list[mailchannels.domain_checks.DkimSetting \| dict[str, str]] \| None` | no | `None` |

#### `mailchannels.domain_checks.CheckDomainResource`

- Kind: `class`
- Summary: Client-bound domain configuration check operations.
- Signature: `mailchannels.domain_checks.CheckDomainResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `check` | `check(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status. |
| `check_async` | `check_async(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check domain configuration status using async HTTP. |

#### `mailchannels.domain_checks.CheckDomainResult`

- Kind: `Pydantic model`
- Summary: Domain configuration check response model.
- Signature: `mailchannels.domain_checks.CheckDomainResult(check_results: mailchannels.domain_checks.CheckResults | None, references: list[str] | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `check_results` | `mailchannels.domain_checks.CheckResults \| None` | no | `None` |
| `references` | `list[str] \| None` | no | `None` |

#### `mailchannels.domain_checks.CheckResults`

- Kind: `Pydantic model`
- Summary: Grouped check results returned by `/check-domain`.
- Signature: `mailchannels.domain_checks.CheckResults(dkim: list[mailchannels.domain_checks.DkimResult] | None, domain_lockdown: mailchannels.domain_checks.LockdownResult | None, sender_domain: mailchannels.domain_checks.SenderDomainResult | None, spf: mailchannels.domain_checks.SpfResult | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `dkim` | `list[mailchannels.domain_checks.DkimResult] \| None` | no | `None` |
| `domain_lockdown` | `mailchannels.domain_checks.LockdownResult \| None` | no | `None` |
| `sender_domain` | `mailchannels.domain_checks.SenderDomainResult \| None` | no | `None` |
| `spf` | `mailchannels.domain_checks.SpfResult \| None` | no | `None` |

#### `mailchannels.domain_checks.DkimResult`

- Kind: `Pydantic model`
- Summary: One DKIM result returned by the domain check endpoint.
- Signature: `mailchannels.domain_checks.DkimResult(dkim_domain: str | None, dkim_selector: str | None, dkim_key_status: str | None, reason: str | None, verdict: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `dkim_domain` | `str \| None` | no | `None` |
| `dkim_selector` | `str \| None` | no | `None` |
| `dkim_key_status` | `str \| None` | no | `None` |
| `reason` | `str \| None` | no | `None` |
| `verdict` | `Optional` | no | `None` |

#### `mailchannels.domain_checks.DkimSetting`

- Kind: `Pydantic model`
- Summary: DKIM settings used by the domain check endpoint.
- Signature: `mailchannels.domain_checks.DkimSetting(dkim_domain: str | None, dkim_selector: str | None, dkim_private_key: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `dkim_domain` | `str \| None` | no | `None` |
| `dkim_selector` | `str \| None` | no | `None` |
| `dkim_private_key` | `str \| None` | no | `None` |

#### `mailchannels.domain_checks.DomainCheckVerdict`

- Kind: `value`
- Summary: 

#### `mailchannels.domain_checks.DomainChecks`

- Kind: `class`
- Summary: Module-level domain configuration check operations.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `check` | `check(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status. |
| `check_async` | `check_async(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check domain configuration status using async HTTP. |

#### `mailchannels.domain_checks.DomainChecksResource`

- Kind: `class`
- Summary: Client-bound domain configuration check operations.
- Signature: `mailchannels.domain_checks.DomainChecksResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `check` | `check(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status. |
| `check_async` | `check_async(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check domain configuration status using async HTTP. |

#### `mailchannels.domain_checks.LockdownResult`

- Kind: `Pydantic model`
- Summary: Domain Lockdown check result.
- Signature: `mailchannels.domain_checks.LockdownResult(reason: str | None, verdict: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `reason` | `str \| None` | no | `None` |
| `verdict` | `Optional` | no | `None` |

#### `mailchannels.domain_checks.SenderDomainResult`

- Kind: `Pydantic model`
- Summary: Sender-domain DNS check result.
- Signature: `mailchannels.domain_checks.SenderDomainResult(a: mailchannels.domain_checks.SenderDomainRecordResult | None, mx: mailchannels.domain_checks.SenderDomainRecordResult | None, verdict: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `a` | `mailchannels.domain_checks.SenderDomainRecordResult \| None` | no | `None` |
| `mx` | `mailchannels.domain_checks.SenderDomainRecordResult \| None` | no | `None` |
| `verdict` | `Optional` | no | `None` |

#### `mailchannels.domain_checks.SpfResult`

- Kind: `Pydantic model`
- Summary: SPF check result.
- Signature: `mailchannels.domain_checks.SpfResult(reason: str | None, spfRecord: str | None, spfRecordError: str | None, verdict: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `reason` | `str \| None` | no | `None` |
| `spfRecord` | `str \| None` | no | `None` |
| `spfRecordError` | `str \| None` | no | `None` |
| `verdict` | `Optional` | no | `None` |

### `mailchannels.check_domain`

Compatibility exports for the documented `/check-domain` endpoint.

#### `mailchannels.check_domain.CheckDomain`

- Kind: `class`
- Summary: Module-level domain configuration check operations.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `check` | `check(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status. |
| `check_async` | `check_async(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check domain configuration status using async HTTP. |

#### `mailchannels.check_domain.CheckDomainParams`

- Kind: `Pydantic model`
- Summary: Request body for `/check-domain`.
- Signature: `mailchannels.check_domain.CheckDomainParams(domain: str, sender_id: str | None, dkim_settings: list[mailchannels.domain_checks.DkimSetting | dict[str, str]] | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `domain` | `str` | yes | `` |
| `sender_id` | `str \| None` | no | `None` |
| `dkim_settings` | `list[mailchannels.domain_checks.DkimSetting \| dict[str, str]] \| None` | no | `None` |

#### `mailchannels.check_domain.CheckDomainResource`

- Kind: `class`
- Summary: Client-bound domain configuration check operations.
- Signature: `mailchannels.check_domain.CheckDomainResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `check` | `check(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status. |
| `check_async` | `check_async(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check domain configuration status using async HTTP. |

#### `mailchannels.check_domain.CheckDomainResult`

- Kind: `Pydantic model`
- Summary: Domain configuration check response model.
- Signature: `mailchannels.check_domain.CheckDomainResult(check_results: mailchannels.domain_checks.CheckResults | None, references: list[str] | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `check_results` | `mailchannels.domain_checks.CheckResults \| None` | no | `None` |
| `references` | `list[str] \| None` | no | `None` |

#### `mailchannels.check_domain.CheckResults`

- Kind: `Pydantic model`
- Summary: Grouped check results returned by `/check-domain`.
- Signature: `mailchannels.check_domain.CheckResults(dkim: list[mailchannels.domain_checks.DkimResult] | None, domain_lockdown: mailchannels.domain_checks.LockdownResult | None, sender_domain: mailchannels.domain_checks.SenderDomainResult | None, spf: mailchannels.domain_checks.SpfResult | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `dkim` | `list[mailchannels.domain_checks.DkimResult] \| None` | no | `None` |
| `domain_lockdown` | `mailchannels.domain_checks.LockdownResult \| None` | no | `None` |
| `sender_domain` | `mailchannels.domain_checks.SenderDomainResult \| None` | no | `None` |
| `spf` | `mailchannels.domain_checks.SpfResult \| None` | no | `None` |

#### `mailchannels.check_domain.DkimResult`

- Kind: `Pydantic model`
- Summary: One DKIM result returned by the domain check endpoint.
- Signature: `mailchannels.check_domain.DkimResult(dkim_domain: str | None, dkim_selector: str | None, dkim_key_status: str | None, reason: str | None, verdict: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `dkim_domain` | `str \| None` | no | `None` |
| `dkim_selector` | `str \| None` | no | `None` |
| `dkim_key_status` | `str \| None` | no | `None` |
| `reason` | `str \| None` | no | `None` |
| `verdict` | `Optional` | no | `None` |

#### `mailchannels.check_domain.DkimSetting`

- Kind: `Pydantic model`
- Summary: DKIM settings used by the domain check endpoint.
- Signature: `mailchannels.check_domain.DkimSetting(dkim_domain: str | None, dkim_selector: str | None, dkim_private_key: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `dkim_domain` | `str \| None` | no | `None` |
| `dkim_selector` | `str \| None` | no | `None` |
| `dkim_private_key` | `str \| None` | no | `None` |

#### `mailchannels.check_domain.DomainCheckVerdict`

- Kind: `value`
- Summary: 

#### `mailchannels.check_domain.DomainChecks`

- Kind: `class`
- Summary: Module-level domain configuration check operations.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `check` | `check(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status. |
| `check_async` | `check_async(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check domain configuration status using async HTTP. |

#### `mailchannels.check_domain.DomainChecksResource`

- Kind: `class`
- Summary: Client-bound domain configuration check operations.
- Signature: `mailchannels.check_domain.DomainChecksResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `check` | `check(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check DKIM, SPF, sender-domain DNS, and Domain Lockdown status. |
| `check_async` | `check_async(domain: str, *, sender_id: str | None = None, dkim_settings: list[DkimSetting | dict[str, str]] | None = None) -> dict[str, Any]` | Check domain configuration status using async HTTP. |

#### `mailchannels.check_domain.LockdownResult`

- Kind: `Pydantic model`
- Summary: Domain Lockdown check result.
- Signature: `mailchannels.check_domain.LockdownResult(reason: str | None, verdict: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `reason` | `str \| None` | no | `None` |
| `verdict` | `Optional` | no | `None` |

#### `mailchannels.check_domain.SenderDomainResult`

- Kind: `Pydantic model`
- Summary: Sender-domain DNS check result.
- Signature: `mailchannels.check_domain.SenderDomainResult(a: mailchannels.domain_checks.SenderDomainRecordResult | None, mx: mailchannels.domain_checks.SenderDomainRecordResult | None, verdict: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `a` | `mailchannels.domain_checks.SenderDomainRecordResult \| None` | no | `None` |
| `mx` | `mailchannels.domain_checks.SenderDomainRecordResult \| None` | no | `None` |
| `verdict` | `Optional` | no | `None` |

#### `mailchannels.check_domain.SpfResult`

- Kind: `Pydantic model`
- Summary: SPF check result.
- Signature: `mailchannels.check_domain.SpfResult(reason: str | None, spfRecord: str | None, spfRecordError: str | None, verdict: Optional)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `reason` | `str \| None` | no | `None` |
| `spfRecord` | `str \| None` | no | `None` |
| `spfRecordError` | `str \| None` | no | `None` |
| `verdict` | `Optional` | no | `None` |

### `mailchannels.dkim`

DKIM resource exports.

#### `mailchannels.dkim.Dkim`

- Kind: `class`
- Summary: Module-level DKIM key management using global SDK configuration.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `create` | `create(domain: str, *, selector: str, algorithm: DkimAlgorithm | None = None, key_length: int | None = None) -> dict[str, Any]` | Create a MailChannels-hosted DKIM key pair for a domain. |
| `create_async` | `create_async(domain: str, *, selector: str, algorithm: DkimAlgorithm | None = None, key_length: int | None = None) -> dict[str, Any]` | Create a MailChannels-hosted DKIM key pair using async HTTP. |
| `list` | `list(domain: str, *, selector: str | None = None, status: DkimKeyStatus | None = None, offset: int | None = None, limit: int | None = None, include_dns_record: bool | None = None) -> dict[str, Any]` | Retrieve MailChannels-hosted DKIM keys for a domain. |
| `list_async` | `list_async(domain: str, *, selector: str | None = None, status: DkimKeyStatus | None = None, offset: int | None = None, limit: int | None = None, include_dns_record: bool | None = None) -> dict[str, Any]` | Retrieve MailChannels-hosted DKIM keys using async HTTP. |
| `rotate` | `rotate(domain: str, selector: str, *, new_selector: str) -> dict[str, Any]` | Rotate a MailChannels-hosted DKIM key pair. |
| `rotate_async` | `rotate_async(domain: str, selector: str, *, new_selector: str) -> dict[str, Any]` | Rotate a MailChannels-hosted DKIM key pair using async HTTP. |
| `update_status` | `update_status(domain: str, selector: str, *, status: DkimUpdateStatus) -> dict[str, Any]` | Update the status of a MailChannels-hosted DKIM key pair. |
| `update_status_async` | `update_status_async(domain: str, selector: str, *, status: DkimUpdateStatus) -> dict[str, Any]` | Update the status of a MailChannels-hosted DKIM key pair using async HTTP. |

#### `mailchannels.dkim.DkimAlgorithm`

- Kind: `value`
- Summary: 

#### `mailchannels.dkim.DkimCreateParams`

- Kind: `TypedDict`
- Summary: Parameters for creating a DKIM key pair.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `algorithm` | `Literal` | no |
| `key_length` | `int` | no |
| `selector` | `str` | no |

#### `mailchannels.dkim.DkimDnsRecord`

- Kind: `Pydantic model`
- Summary: Suggested DKIM DNS record returned by MailChannels.
- Signature: `mailchannels.dkim.DkimDnsRecord(name: str, type: str, value: str)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `name` | `str` | yes | `` |
| `type` | `str` | yes | `` |
| `value` | `str` | yes | `` |

#### `mailchannels.dkim.DkimKeyInfo`

- Kind: `Pydantic model`
- Summary: MailChannels-hosted DKIM key metadata.
- Signature: `mailchannels.dkim.DkimKeyInfo(domain: str, selector: str, public_key: str, status: Literal, algorithm: str, key_length: int | None, dkim_dns_records: list[mailchannels.dkim.DkimDnsRecord] | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `domain` | `str` | yes | `` |
| `selector` | `str` | yes | `` |
| `public_key` | `str` | yes | `` |
| `status` | `Literal` | yes | `` |
| `algorithm` | `str` | yes | `` |
| `key_length` | `int \| None` | no | `None` |
| `dkim_dns_records` | `list[mailchannels.dkim.DkimDnsRecord] \| None` | no | `None` |

#### `mailchannels.dkim.DkimKeyList`

- Kind: `Pydantic model`
- Summary: Response model for listing MailChannels-hosted DKIM keys.
- Signature: `mailchannels.dkim.DkimKeyList(keys: list)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `keys` | `list` | yes | `` |

#### `mailchannels.dkim.DkimKeyStatus`

- Kind: `value`
- Summary: 

#### `mailchannels.dkim.DkimListParams`

- Kind: `TypedDict`
- Summary: Query parameters for retrieving DKIM key pairs.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `include_dns_record` | `bool` | no |
| `limit` | `int` | no |
| `offset` | `int` | no |
| `selector` | `str` | no |
| `status` | `Literal` | no |

#### `mailchannels.dkim.DkimResource`

- Kind: `class`
- Summary: Client-bound DKIM key management operations.
- Signature: `mailchannels.dkim.DkimResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `create` | `create(domain: str, *, selector: str, algorithm: DkimAlgorithm | None = None, key_length: int | None = None) -> dict[str, Any]` | Create a MailChannels-hosted DKIM key pair for a domain. |
| `create_async` | `create_async(domain: str, *, selector: str, algorithm: DkimAlgorithm | None = None, key_length: int | None = None) -> dict[str, Any]` | Create a MailChannels-hosted DKIM key pair using async HTTP. |
| `list` | `list(domain: str, *, selector: str | None = None, status: DkimKeyStatus | None = None, offset: int | None = None, limit: int | None = None, include_dns_record: bool | None = None) -> dict[str, Any]` | Retrieve MailChannels-hosted DKIM keys for a domain. |
| `list_async` | `list_async(domain: str, *, selector: str | None = None, status: DkimKeyStatus | None = None, offset: int | None = None, limit: int | None = None, include_dns_record: bool | None = None) -> dict[str, Any]` | Retrieve MailChannels-hosted DKIM keys using async HTTP. |
| `rotate` | `rotate(domain: str, selector: str, *, new_selector: str) -> dict[str, Any]` | Rotate a MailChannels-hosted DKIM key pair. |
| `rotate_async` | `rotate_async(domain: str, selector: str, *, new_selector: str) -> dict[str, Any]` | Rotate a MailChannels-hosted DKIM key pair using async HTTP. |
| `update_status` | `update_status(domain: str, selector: str, *, status: DkimUpdateStatus) -> dict[str, Any]` | Update the status of a MailChannels-hosted DKIM key pair. |
| `update_status_async` | `update_status_async(domain: str, selector: str, *, status: DkimUpdateStatus) -> dict[str, Any]` | Update the status of a MailChannels-hosted DKIM key pair using async HTTP. |

#### `mailchannels.dkim.DkimRotateResponse`

- Kind: `Pydantic model`
- Summary: Response model for DKIM key rotation.
- Signature: `mailchannels.dkim.DkimRotateResponse(new_key: DkimKeyInfo, rotated_key: DkimKeyInfo)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `new_key` | `DkimKeyInfo` | yes | `` |
| `rotated_key` | `DkimKeyInfo` | yes | `` |

#### `mailchannels.dkim.DkimUpdateStatus`

- Kind: `value`
- Summary: 

### `mailchannels.metrics`

Metrics resource exports.

#### `mailchannels.metrics.Metrics`

- Kind: `class`
- Summary: Module-level metrics operations using global SDK configuration.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `engagement` | `engagement(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve engagement metrics. |
| `engagement_async` | `engagement_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve engagement metrics using async HTTP. |
| `performance` | `performance(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve performance metrics. |
| `performance_async` | `performance_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve performance metrics using async HTTP. |
| `recipient_behavior` | `recipient_behavior(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve recipient behaviour metrics using US spelling. |
| `recipient_behavior_async` | `recipient_behavior_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve recipient behaviour metrics using US spelling and async HTTP. |
| `recipient_behaviour` | `recipient_behaviour(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve recipient behaviour metrics. |
| `recipient_behaviour_async` | `recipient_behaviour_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve recipient behaviour metrics using async HTTP. |
| `senders` | `senders(sender_type: MetricsSenderType, *, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, limit: int | None = None, offset: int | None = None, sort_order: MetricsSortOrder | None = None) -> dict[str, Any]` | Retrieve sender metrics grouped by campaigns or sub-accounts. |
| `senders_async` | `senders_async(sender_type: MetricsSenderType, *, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, limit: int | None = None, offset: int | None = None, sort_order: MetricsSortOrder | None = None) -> dict[str, Any]` | Retrieve sender metrics using async HTTP. |
| `volume` | `volume(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve volume metrics. |
| `volume_async` | `volume_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve volume metrics using async HTTP. |

#### `mailchannels.metrics.MetricsBucket`

- Kind: `Pydantic model`
- Summary: One time bucket in a metrics response.
- Signature: `mailchannels.metrics.MetricsBucket(count: int, period_start: str)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `count` | `int` | yes | `` |
| `period_start` | `str` | yes | `` |

#### `mailchannels.metrics.MetricsEngagement`

- Kind: `Pydantic model`
- Summary: Engagement metrics response model.
- Signature: `mailchannels.metrics.MetricsEngagement(open: int, open_tracking_delivered: int, click: int, click_tracking_delivered: int, buckets: dict)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `open` | `int` | yes | `` |
| `open_tracking_delivered` | `int` | yes | `` |
| `click` | `int` | yes | `` |
| `click_tracking_delivered` | `int` | yes | `` |
| `buckets` | `dict` | yes | `` |

#### `mailchannels.metrics.MetricsInterval`

- Kind: `value`
- Summary: 

#### `mailchannels.metrics.MetricsPerformance`

- Kind: `Pydantic model`
- Summary: Performance metrics response model.
- Signature: `mailchannels.metrics.MetricsPerformance(processed: int, delivered: int, bounced: int, buckets: dict)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `processed` | `int` | yes | `` |
| `delivered` | `int` | yes | `` |
| `bounced` | `int` | yes | `` |
| `buckets` | `dict` | yes | `` |

#### `mailchannels.metrics.MetricsQueryParams`

- Kind: `TypedDict`
- Summary: Query parameters shared by time-series metrics endpoints.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `campaign_id` | `str` | no |
| `end_time` | `Union` | no |
| `interval` | `Literal` | no |
| `start_time` | `Union` | no |

#### `mailchannels.metrics.MetricsRecipientBehaviour`

- Kind: `Pydantic model`
- Summary: Recipient behaviour metrics response model.
- Signature: `mailchannels.metrics.MetricsRecipientBehaviour(unsubscribed: int, unsubscribe_delivered: int, buckets: dict)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `unsubscribed` | `int` | yes | `` |
| `unsubscribe_delivered` | `int` | yes | `` |
| `buckets` | `dict` | yes | `` |

#### `mailchannels.metrics.MetricsResource`

- Kind: `class`
- Summary: Client-bound metrics operations.
- Signature: `mailchannels.metrics.MetricsResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `engagement` | `engagement(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve engagement metrics. |
| `engagement_async` | `engagement_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve engagement metrics using async HTTP. |
| `performance` | `performance(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve performance metrics. |
| `performance_async` | `performance_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve performance metrics using async HTTP. |
| `recipient_behavior` | `recipient_behavior(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve recipient behaviour metrics using US spelling. |
| `recipient_behavior_async` | `recipient_behavior_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve recipient behaviour metrics using US spelling and async HTTP. |
| `recipient_behaviour` | `recipient_behaviour(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve recipient behaviour metrics. |
| `recipient_behaviour_async` | `recipient_behaviour_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve recipient behaviour metrics using async HTTP. |
| `senders` | `senders(sender_type: MetricsSenderType, *, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, limit: int | None = None, offset: int | None = None, sort_order: MetricsSortOrder | None = None) -> dict[str, Any]` | Retrieve sender metrics grouped by campaigns or sub-accounts. |
| `senders_async` | `senders_async(sender_type: MetricsSenderType, *, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, limit: int | None = None, offset: int | None = None, sort_order: MetricsSortOrder | None = None) -> dict[str, Any]` | Retrieve sender metrics using async HTTP. |
| `volume` | `volume(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve volume metrics. |
| `volume_async` | `volume_async(*, start_time: MetricsTime | None = None, end_time: MetricsTime | None = None, campaign_id: str | None = None, interval: MetricsInterval | None = None) -> dict[str, Any]` | Retrieve volume metrics using async HTTP. |

#### `mailchannels.metrics.MetricsSender`

- Kind: `Pydantic model`
- Summary: One sender row in a sender metrics response.
- Signature: `mailchannels.metrics.MetricsSender(name: str, processed: int, delivered: int, dropped: int, bounced: int)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `name` | `str` | yes | `` |
| `processed` | `int` | yes | `` |
| `delivered` | `int` | yes | `` |
| `dropped` | `int` | yes | `` |
| `bounced` | `int` | yes | `` |

#### `mailchannels.metrics.MetricsSenderQueryParams`

- Kind: `TypedDict`
- Summary: Query parameters for sender metrics endpoints.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `end_time` | `Union` | no |
| `limit` | `int` | no |
| `offset` | `int` | no |
| `sort_order` | `Literal` | no |
| `start_time` | `Union` | no |

#### `mailchannels.metrics.MetricsSenderResponse`

- Kind: `Pydantic model`
- Summary: Sender metrics response model.
- Signature: `mailchannels.metrics.MetricsSenderResponse(limit: int, offset: int, total: int, senders: list)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `limit` | `int` | yes | `` |
| `offset` | `int` | yes | `` |
| `total` | `int` | yes | `` |
| `senders` | `list` | yes | `` |

#### `mailchannels.metrics.MetricsSenderType`

- Kind: `value`
- Summary: 

#### `mailchannels.metrics.MetricsSortOrder`

- Kind: `value`
- Summary: 

#### `mailchannels.metrics.MetricsTime`

- Kind: `value`
- Summary: 

#### `mailchannels.metrics.MetricsVolume`

- Kind: `Pydantic model`
- Summary: Volume metrics response model.
- Signature: `mailchannels.metrics.MetricsVolume(processed: int, delivered: int, dropped: int, buckets: dict)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `processed` | `int` | yes | `` |
| `delivered` | `int` | yes | `` |
| `dropped` | `int` | yes | `` |
| `buckets` | `dict` | yes | `` |

### `mailchannels.sub_accounts`

Sub-account resource exports.

#### `mailchannels.sub_accounts.ApiKey`

- Kind: `Pydantic model`
- Summary: MailChannels sub-account API key response model.
- Signature: `mailchannels.sub_accounts.ApiKey()`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |

#### `mailchannels.sub_accounts.CreateSubAccountParams`

- Kind: `TypedDict`
- Summary: Parameters for creating a MailChannels sub-account.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `company_name` | `str` | no |
| `handle` | `str` | no |

#### `mailchannels.sub_accounts.SetLimitParams`

- Kind: `TypedDict`
- Summary: Parameters for setting a sub-account sending limit.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `sends` | `int` | yes |

#### `mailchannels.sub_accounts.SmtpPassword`

- Kind: `Pydantic model`
- Summary: MailChannels sub-account SMTP password response model.
- Signature: `mailchannels.sub_accounts.SmtpPassword()`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |

#### `mailchannels.sub_accounts.SubAccount`

- Kind: `Pydantic model`
- Summary: MailChannels sub-account response model.
- Signature: `mailchannels.sub_accounts.SubAccount(handle: str | None, company_name: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `handle` | `str \| None` | no | `None` |
| `company_name` | `str \| None` | no | `None` |

#### `mailchannels.sub_accounts.SubAccountApiKeysResource`

- Kind: `class`
- Summary: Client-bound sub-account API key operations.
- Signature: `mailchannels.sub_accounts.SubAccountApiKeysResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `create` | `create(handle: str) -> dict[str, Any]` | Create an API key for a sub-account. |
| `create_async` | `create_async(handle: str) -> dict[str, Any]` | Create an API key for a sub-account using async HTTP. |
| `delete` | `delete(handle: str, key_id: str) -> dict[str, Any]` | Delete an API key from a sub-account. |
| `delete_async` | `delete_async(handle: str, key_id: str) -> dict[str, Any]` | Delete an API key from a sub-account using async HTTP. |
| `list` | `list(handle: str) -> dict[str, Any]` | Retrieve API keys for a sub-account. |
| `list_async` | `list_async(handle: str) -> dict[str, Any]` | Retrieve API keys for a sub-account using async HTTP. |

#### `mailchannels.sub_accounts.SubAccountLimit`

- Kind: `Pydantic model`
- Summary: MailChannels sub-account sending limit response model.
- Signature: `mailchannels.sub_accounts.SubAccountLimit(sends: int | None, monthly_limit: int | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `sends` | `int \| None` | no | `None` |
| `monthly_limit` | `int \| None` | no | `None` |

#### `mailchannels.sub_accounts.SubAccountLimitsResource`

- Kind: `class`
- Summary: Client-bound sub-account sending limit operations.
- Signature: `mailchannels.sub_accounts.SubAccountLimitsResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `delete` | `delete(handle: str) -> dict[str, Any]` | Delete the sending limit for a sub-account. |
| `delete_async` | `delete_async(handle: str) -> dict[str, Any]` | Delete the sending limit for a sub-account using async HTTP. |
| `retrieve` | `retrieve(handle: str) -> dict[str, Any]` | Retrieve the sending limit for a sub-account. |
| `retrieve_async` | `retrieve_async(handle: str) -> dict[str, Any]` | Retrieve the sending limit for a sub-account using async HTTP. |
| `set` | `set(handle: str, *, sends: int | None = None, monthly_limit: int | None = None) -> dict[str, Any]` | Set the monthly sending limit for a sub-account. |
| `set_async` | `set_async(handle: str, *, sends: int | None = None, monthly_limit: int | None = None) -> dict[str, Any]` | Set the monthly sending limit for a sub-account using async HTTP. |

#### `mailchannels.sub_accounts.SubAccountSmtpPasswordsResource`

- Kind: `class`
- Summary: Client-bound sub-account SMTP password operations.
- Signature: `mailchannels.sub_accounts.SubAccountSmtpPasswordsResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `create` | `create(handle: str) -> dict[str, Any]` | Create an SMTP password for a sub-account. |
| `create_async` | `create_async(handle: str) -> dict[str, Any]` | Create an SMTP password for a sub-account using async HTTP. |
| `delete` | `delete(handle: str, password_id: str) -> dict[str, Any]` | Delete an SMTP password from a sub-account. |
| `delete_async` | `delete_async(handle: str, password_id: str) -> dict[str, Any]` | Delete an SMTP password from a sub-account using async HTTP. |
| `list` | `list(handle: str) -> dict[str, Any]` | Retrieve SMTP passwords for a sub-account. |
| `list_async` | `list_async(handle: str) -> dict[str, Any]` | Retrieve SMTP passwords for a sub-account using async HTTP. |

#### `mailchannels.sub_accounts.SubAccounts`

- Kind: `class`
- Summary: Module-level sub-account operations using global SDK configuration.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `activate` | `activate(handle: str) -> dict[str, Any]` | Activate a suspended sub-account. |
| `activate_async` | `activate_async(handle: str) -> dict[str, Any]` | Activate a suspended sub-account using async HTTP. |
| `create` | `create(*, company_name: str | None = None, handle: str | None = None) -> dict[str, Any]` | Create a sub-account under the parent account. |
| `create_async` | `create_async(*, company_name: str | None = None, handle: str | None = None) -> dict[str, Any]` | Create a sub-account under the parent account using async HTTP. |
| `delete` | `delete(handle: str) -> dict[str, Any]` | Delete a sub-account. |
| `delete_async` | `delete_async(handle: str) -> dict[str, Any]` | Delete a sub-account using async HTTP. |
| `list` | `list(*, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve sub-accounts for the parent account. |
| `list_async` | `list_async(*, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve sub-accounts for the parent account using async HTTP. |
| `retrieve_usage` | `retrieve_usage(handle: str) -> dict[str, Any]` | Retrieve usage statistics for a sub-account. |
| `retrieve_usage_async` | `retrieve_usage_async(handle: str) -> dict[str, Any]` | Retrieve usage statistics for a sub-account using async HTTP. |
| `suspend` | `suspend(handle: str) -> dict[str, Any]` | Suspend a sub-account. |
| `suspend_async` | `suspend_async(handle: str) -> dict[str, Any]` | Suspend a sub-account using async HTTP. |

#### `mailchannels.sub_accounts.SubAccountsResource`

- Kind: `class`
- Summary: Client-bound sub-account operations.
- Signature: `mailchannels.sub_accounts.SubAccountsResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `activate` | `activate(handle: str) -> dict[str, Any]` | Activate a suspended sub-account. |
| `activate_async` | `activate_async(handle: str) -> dict[str, Any]` | Activate a suspended sub-account using async HTTP. |
| `create` | `create(*, company_name: str | None = None, handle: str | None = None) -> dict[str, Any]` | Create a sub-account under the parent account. |
| `create_async` | `create_async(*, company_name: str | None = None, handle: str | None = None) -> dict[str, Any]` | Create a sub-account under the parent account using async HTTP. |
| `delete` | `delete(handle: str) -> dict[str, Any]` | Delete a sub-account. |
| `delete_async` | `delete_async(handle: str) -> dict[str, Any]` | Delete a sub-account using async HTTP. |
| `list` | `list(*, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve sub-accounts for the parent account. |
| `list_async` | `list_async(*, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve sub-accounts for the parent account using async HTTP. |
| `retrieve_usage` | `retrieve_usage(handle: str) -> dict[str, Any]` | Retrieve usage statistics for a sub-account. |
| `retrieve_usage_async` | `retrieve_usage_async(handle: str) -> dict[str, Any]` | Retrieve usage statistics for a sub-account using async HTTP. |
| `suspend` | `suspend(handle: str) -> dict[str, Any]` | Suspend a sub-account. |
| `suspend_async` | `suspend_async(handle: str) -> dict[str, Any]` | Suspend a sub-account using async HTTP. |

#### `mailchannels.sub_accounts.UsageStats`

- Kind: `Pydantic model`
- Summary: MailChannels usage response model.
- Signature: `mailchannels.sub_accounts.UsageStats()`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |

### `mailchannels.suppressions`

Suppression list resource exports.

#### `mailchannels.suppressions.SuppressionDeleteSource`

- Kind: `value`
- Summary: 

#### `mailchannels.suppressions.SuppressionEntry`

- Kind: `Pydantic model`
- Summary: Suppression entry returned by MailChannels.
- Signature: `mailchannels.suppressions.SuppressionEntry(recipient: str, suppression_types: list[Literal['transactional', 'non-transactional']] | None, notes: str | None, source: Optional, sender: str | None, created_at: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `recipient` | `str` | yes | `` |
| `suppression_types` | `list[Literal['transactional', 'non-transactional']] \| None` | no | `None` |
| `notes` | `str \| None` | no | `None` |
| `source` | `Optional` | no | `None` |
| `sender` | `str \| None` | no | `None` |
| `created_at` | `str \| None` | no | `None` |

#### `mailchannels.suppressions.SuppressionEntryParams`

- Kind: `TypedDict`
- Summary: One suppression entry to create.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `notes` | `str \| None` | no |
| `recipient` | `str` | no |
| `suppression_types` | `list` | no |

#### `mailchannels.suppressions.SuppressionListResponse`

- Kind: `Pydantic model`
- Summary: Response model for suppression list retrieval.
- Signature: `mailchannels.suppressions.SuppressionListResponse(suppression_list: list)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `suppression_list` | `list` | yes | `` |

#### `mailchannels.suppressions.SuppressionSource`

- Kind: `value`
- Summary: 

#### `mailchannels.suppressions.SuppressionType`

- Kind: `value`
- Summary: 

#### `mailchannels.suppressions.Suppressions`

- Kind: `class`
- Summary: Module-level suppression list operations.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `create` | `create(entries: list_type[SuppressionEntryParams], *, add_to_sub_accounts: bool | None = None) -> dict[str, Any]` | Create suppression entries. |
| `create_async` | `create_async(entries: list_type[SuppressionEntryParams], *, add_to_sub_accounts: bool | None = None) -> dict[str, Any]` | Create suppression entries using async HTTP. |
| `delete` | `delete(recipient: str, *, source: SuppressionDeleteSource | None = None) -> dict[str, Any]` | Delete suppression entries for a recipient. |
| `delete_async` | `delete_async(recipient: str, *, source: SuppressionDeleteSource | None = None) -> dict[str, Any]` | Delete suppression entries for a recipient using async HTTP. |
| `list` | `list(**kwargs: Any) -> dict[str, Any]` | Retrieve suppression entries. |
| `list_async` | `list_async(**kwargs: Any) -> dict[str, Any]` | Retrieve suppression entries using async HTTP. |

#### `mailchannels.suppressions.SuppressionsResource`

- Kind: `class`
- Summary: Client-bound suppression list operations.
- Signature: `mailchannels.suppressions.SuppressionsResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `create` | `create(entries: list_type[SuppressionEntryParams], *, add_to_sub_accounts: bool | None = None) -> dict[str, Any]` | Create suppression entries. |
| `create_async` | `create_async(entries: list_type[SuppressionEntryParams], *, add_to_sub_accounts: bool | None = None) -> dict[str, Any]` | Create suppression entries using async HTTP. |
| `delete` | `delete(recipient: str, *, source: SuppressionDeleteSource | None = None) -> dict[str, Any]` | Delete suppression entries for a recipient. |
| `delete_async` | `delete_async(recipient: str, *, source: SuppressionDeleteSource | None = None) -> dict[str, Any]` | Delete suppression entries for a recipient using async HTTP. |
| `list` | `list(*, recipient: str | None = None, source: SuppressionSource | None = None, created_before: str | None = None, created_after: str | None = None, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve suppression entries. |
| `list_async` | `list_async(*, recipient: str | None = None, source: SuppressionSource | None = None, created_before: str | None = None, created_after: str | None = None, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve suppression entries using async HTTP. |

### `mailchannels.usage`

Usage resource exports.

#### `mailchannels.usage.Usage`

- Kind: `class`
- Summary: Module-level parent-account usage operations.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `retrieve` | `retrieve() -> dict[str, Any]` | Retrieve parent-account usage for the current billing period. |
| `retrieve_async` | `retrieve_async() -> dict[str, Any]` | Retrieve parent-account usage using async HTTP. |

#### `mailchannels.usage.UsageResource`

- Kind: `class`
- Summary: Client-bound parent-account usage operations.
- Signature: `mailchannels.usage.UsageResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `retrieve` | `retrieve() -> dict[str, Any]` | Retrieve parent-account usage for the current billing period. |
| `retrieve_async` | `retrieve_async() -> dict[str, Any]` | Retrieve parent-account usage using async HTTP. |

#### `mailchannels.usage.UsageStats`

- Kind: `Pydantic model`
- Summary: MailChannels usage statistics for the current billing period.
- Signature: `mailchannels.usage.UsageStats(total_usage: int, period_start_date: str | None, period_end_date: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `total_usage` | `int` | yes | `` |
| `period_start_date` | `str \| None` | no | `None` |
| `period_end_date` | `str \| None` | no | `None` |

### `mailchannels.webhooks`

Webhook resources for the MailChannels SDK.

#### `mailchannels.webhooks.SignatureParameters`

- Kind: `Pydantic model`
- Summary: Parsed metadata from a MailChannels Signature-Input header.
- Signature: `mailchannels.webhooks.SignatureParameters(signature_name: str, covered_components: list, created: int | None, algorithm: str | None, key_id: str | None, raw: str)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `signature_name` | `str` | yes | `` |
| `covered_components` | `list` | yes | `` |
| `created` | `int \| None` | no | `None` |
| `algorithm` | `str \| None` | no | `None` |
| `key_id` | `str \| None` | no | `None` |
| `raw` | `str` | yes | `` |

#### `mailchannels.webhooks.Webhook`

- Kind: `Pydantic model`
- Summary: A configured MailChannels webhook endpoint.
- Signature: `mailchannels.webhooks.Webhook(webhook: str)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `webhook` | `str` | yes | `` |

#### `mailchannels.webhooks.WebhookBatch`

- Kind: `Pydantic model`
- Summary: One MailChannels webhook batch delivery attempt.
- Signature: `mailchannels.webhooks.WebhookBatch(batch_id: int, customer_handle: str, webhook: str, status: str, created_at: str, event_count: int, duration: mailchannels.webhooks.WebhookBatchDuration | None, status_code: int | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `batch_id` | `int` | yes | `` |
| `customer_handle` | `str` | yes | `` |
| `webhook` | `str` | yes | `` |
| `status` | `str` | yes | `` |
| `created_at` | `str` | yes | `` |
| `event_count` | `int` | yes | `` |
| `duration` | `mailchannels.webhooks.WebhookBatchDuration \| None` | no | `None` |
| `status_code` | `int \| None` | no | `None` |

#### `mailchannels.webhooks.WebhookBatchDuration`

- Kind: `Pydantic model`
- Summary: Duration metadata for a webhook batch delivery attempt.
- Signature: `mailchannels.webhooks.WebhookBatchDuration(value: int, unit: Literal)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `value` | `int` | yes | `` |
| `unit` | `Literal` | yes | `` |

#### `mailchannels.webhooks.WebhookBatchResult`

- Kind: `Pydantic model`
- Summary: Paged webhook batch result.
- Signature: `mailchannels.webhooks.WebhookBatchResult(webhook_batches: list)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `webhook_batches` | `list` | yes | `` |

#### `mailchannels.webhooks.WebhookBatchStatus`

- Kind: `value`
- Summary: 

#### `mailchannels.webhooks.WebhookEvent`

- Kind: `value`
- Summary: 

#### `mailchannels.webhooks.WebhookEventPayload`

- Kind: `Pydantic model`
- Summary: Common fields present on MailChannels delivery event payloads.
- Signature: `mailchannels.webhooks.WebhookEventPayload(email: str | None, customer_handle: str, timestamp: int, event: Union, request_id: str | None, smtp_id: str | None, recipients: list[str] | None, status: str | None, reason: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `email` | `str \| None` | no | `None` |
| `customer_handle` | `str` | yes | `` |
| `timestamp` | `int` | yes | `` |
| `event` | `Union` | yes | `` |
| `request_id` | `str \| None` | no | `None` |
| `smtp_id` | `str \| None` | no | `None` |
| `recipients` | `list[str] \| None` | no | `None` |
| `status` | `str \| None` | no | `None` |
| `reason` | `str \| None` | no | `None` |

#### `mailchannels.webhooks.WebhookHeaders`

- Kind: `value`
- Summary: 

#### `mailchannels.webhooks.WebhookPayload`

- Kind: `value`
- Summary: 

#### `mailchannels.webhooks.WebhookPublicKey`

- Kind: `Pydantic model`
- Summary: Webhook public signing key returned by MailChannels.
- Signature: `mailchannels.webhooks.WebhookPublicKey(id: str, key: str)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `id` | `str` | yes | `` |
| `key` | `str` | yes | `` |

#### `mailchannels.webhooks.WebhookValidationRequest`

- Kind: `TypedDict`
- Summary: Request body used to validate enrolled webhooks.

Fields:

| Field | Type | Required |
| --- | --- | --- |
| `request_id` | `str` | no |

#### `mailchannels.webhooks.WebhookValidationResponse`

- Kind: `Pydantic model`
- Summary: HTTP response returned by a validated webhook endpoint.
- Signature: `mailchannels.webhooks.WebhookValidationResponse(status: int, body: str | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `status` | `int` | yes | `` |
| `body` | `str \| None` | no | `None` |

#### `mailchannels.webhooks.WebhookValidationResult`

- Kind: `Pydantic model`
- Summary: Validation result for one webhook endpoint.
- Signature: `mailchannels.webhooks.WebhookValidationResult(webhook: str, result: Literal, response: mailchannels.webhooks.WebhookValidationResponse | None)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `webhook` | `str` | yes | `` |
| `result` | `Literal` | yes | `` |
| `response` | `mailchannels.webhooks.WebhookValidationResponse \| None` | no | `None` |

#### `mailchannels.webhooks.WebhookValidationResults`

- Kind: `Pydantic model`
- Summary: Validation results for enrolled webhook endpoints.
- Signature: `mailchannels.webhooks.WebhookValidationResults(all_passed: bool, results: list)`

Fields:

| Field | Type | Required | Default |
| --- | --- | --- | --- |
| `all_passed` | `bool` | yes | `` |
| `results` | `list` | yes | `` |

#### `mailchannels.webhooks.Webhooks`

- Kind: `class`
- Summary: Module-level webhook operations using global SDK configuration.

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `batches` | `batches(*, created_after: str | None = None, created_before: str | None = None, statuses: list_type[WebhookBatchStatus] | None = None, webhook: str | None = None, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve webhook delivery batches. |
| `batches_async` | `batches_async(*, created_after: str | None = None, created_before: str | None = None, statuses: list_type[WebhookBatchStatus] | None = None, webhook: str | None = None, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve webhook delivery batches using async HTTP. |
| `create` | `create(endpoint: str) -> dict[str, Any]` | Enroll a webhook endpoint for delivery events. |
| `create_async` | `create_async(endpoint: str) -> dict[str, Any]` | Enroll a webhook endpoint for delivery events using async HTTP. |
| `delete` | `delete() -> dict[str, Any]` | Delete all configured webhook endpoints. |
| `delete_async` | `delete_async() -> dict[str, Any]` | Delete all configured webhook endpoints using async HTTP. |
| `list` | `list() -> dict[str, Any]` | Retrieve configured webhook endpoints. |
| `list_async` | `list_async() -> dict[str, Any]` | Retrieve configured webhook endpoints using async HTTP. |
| `parse_signature_input` | `parse_signature_input(value: str) -> SignatureParameters` | Parse a MailChannels RFC 9421 Signature-Input header value. |
| `public_key` | `public_key(key_id: str) -> dict[str, Any]` | Retrieve a webhook public signing key by ID. |
| `public_key_async` | `public_key_async(key_id: str) -> dict[str, Any]` | Retrieve a webhook public signing key by ID using async HTTP. |
| `resend_batch` | `resend_batch(batch_id: int, *, customer_handle: str) -> dict[str, Any]` | Synchronously resend one webhook batch. |
| `resend_batch_async` | `resend_batch_async(batch_id: int, *, customer_handle: str) -> dict[str, Any]` | Synchronously resend one webhook batch using async HTTP. |
| `signature_is_fresh` | `signature_is_fresh(parameters: SignatureParameters, *, tolerance_seconds: int = 300, now: int | None = None) -> bool` | Return whether a signature timestamp is within the allowed age. |
| `signature_key_id` | `signature_key_id(headers: dict[str, str]) -> str | None` | Extract the signing key ID from webhook headers. |
| `validate` | `validate(*, request_id: str | None = None) -> dict[str, Any]` | Validate enrolled webhook endpoints with a test event. |
| `validate_async` | `validate_async(*, request_id: str | None = None) -> dict[str, Any]` | Validate enrolled webhook endpoints with a test event using async HTTP. |
| `verify_content_digest` | `verify_content_digest(headers: dict[str, str], body: bytes | str) -> bool` | Verify the webhook Content-Digest header against the raw body. |

#### `mailchannels.webhooks.WebhooksResource`

- Kind: `class`
- Summary: Client-bound webhook operations.
- Signature: `mailchannels.webhooks.WebhooksResource(client: Any) -> None`

Methods:

| Method | Signature | Summary |
| --- | --- | --- |
| `batches` | `batches(*, created_after: str | None = None, created_before: str | None = None, statuses: list_type[WebhookBatchStatus] | None = None, webhook: str | None = None, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve webhook delivery batches. |
| `batches_async` | `batches_async(*, created_after: str | None = None, created_before: str | None = None, statuses: list_type[WebhookBatchStatus] | None = None, webhook: str | None = None, limit: int | None = None, offset: int | None = None) -> dict[str, Any]` | Retrieve webhook delivery batches using async HTTP. |
| `create` | `create(endpoint: str) -> dict[str, Any]` | Enroll a webhook endpoint for delivery events. |
| `create_async` | `create_async(endpoint: str) -> dict[str, Any]` | Enroll a webhook endpoint for delivery events using async HTTP. |
| `delete` | `delete() -> dict[str, Any]` | Delete all configured webhook endpoints. |
| `delete_async` | `delete_async() -> dict[str, Any]` | Delete all configured webhook endpoints using async HTTP. |
| `list` | `list() -> dict[str, Any]` | Retrieve configured webhook endpoints. |
| `list_async` | `list_async() -> dict[str, Any]` | Retrieve configured webhook endpoints using async HTTP. |
| `public_key` | `public_key(key_id: str) -> dict[str, Any]` | Retrieve a webhook public signing key by ID. |
| `public_key_async` | `public_key_async(key_id: str) -> dict[str, Any]` | Retrieve a webhook public signing key by ID using async HTTP. |
| `resend_batch` | `resend_batch(batch_id: int, *, customer_handle: str) -> dict[str, Any]` | Synchronously resend one webhook batch. |
| `resend_batch_async` | `resend_batch_async(batch_id: int, *, customer_handle: str) -> dict[str, Any]` | Synchronously resend one webhook batch using async HTTP. |
| `validate` | `validate(*, request_id: str | None = None) -> dict[str, Any]` | Validate enrolled webhook endpoints with a test event. |
| `validate_async` | `validate_async(*, request_id: str | None = None) -> dict[str, Any]` | Validate enrolled webhook endpoints with a test event using async HTTP. |

#### `mailchannels.webhooks.parse_signature_input`

- Kind: `function`
- Summary: Parse a MailChannels RFC 9421 Signature-Input header value.
- Signature: `mailchannels.webhooks.parse_signature_input(value: str) -> SignatureParameters`

#### `mailchannels.webhooks.signature_is_fresh`

- Kind: `function`
- Summary: Return whether a signature timestamp is within the allowed age.
- Signature: `mailchannels.webhooks.signature_is_fresh(parameters: SignatureParameters, *, tolerance_seconds: int = 300, now: int | None = None) -> bool`

#### `mailchannels.webhooks.signature_key_id`

- Kind: `function`
- Summary: Extract the signing key ID from webhook headers.
- Signature: `mailchannels.webhooks.signature_key_id(headers: dict[str, str]) -> str | None`

#### `mailchannels.webhooks.verify_content_digest`

- Kind: `function`
- Summary: Verify the webhook Content-Digest header against the raw request body.
- Signature: `mailchannels.webhooks.verify_content_digest(headers: dict[str, str], body: bytes | str) -> bool`

