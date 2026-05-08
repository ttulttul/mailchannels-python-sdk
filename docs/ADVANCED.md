# Advanced Usage

This document covers SDK behavior that is useful in production code but too
detailed for the README quick path.

## Strict Response Models

The default SDK response remains dict-like and supports attribute access:

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

Explicit clients created with `Client(strict_responses=True)` expose Pydantic
model return types to type checkers. Module-level helpers keep broader return
types because `mailchannels.strict_responses` is mutable runtime configuration.
For email sends, strict mode validates `/send` normal responses as
`SendResponse(request_id=..., results=[...])`, `/send` dry-run responses as
`SendResponse(data=[...])`, and `/send-async` responses as
`QueuedSendResponse(request_id=..., queued_at=...)`.

```python
client = mailchannels.Client(
    api_key="YOUR-API-KEY",
    strict_responses=True,
)

usage = client.usage.retrieve()

print(usage.total_usage)
print(usage.http_headers)
```

## Version And API Compatibility

The package exports its version so applications can log it at startup or include
it in diagnostics. The SDK uses the same value in its `User-Agent` header.

```python
import mailchannels

print(mailchannels.__version__)
print(mailchannels.get_version())
```

The SDK also exports the MailChannels OpenAPI document metadata that this
release was checked against. This is useful for support tickets, release audits,
and startup diagnostics.

```python
print(mailchannels.API_SPEC_COMPATIBILITY.to_dict())
```

`API_SPEC_COMPATIBILITY` is an immutable `ApiSpecCompatibility` value with
`source_url`, `openapi_version`, `sha256`, `checked_at`, and `sdk_version`
fields.

## Client Lifecycle

The default synchronous transport keeps one `requests.Session` per SDK
transport, and the default async transport keeps one lazily-created
`httpx.AsyncClient` per SDK transport. Reuse a `Client` instance when sending
multiple requests so connection pooling and TLS reuse can work.

Close long-lived clients with `client.close()` for sync clients or
`await client.aclose()` for async clients. Clients also support sync and async
context-manager protocols.

## Custom Transports

If your application needs custom retry behavior, instrumentation, test
isolation, or a framework-specific HTTP stack, pass a transport object that
implements the `SyncHTTPClient` or `AsyncHTTPClient` protocol. The `request()`
method must accept `method`, `url`, `headers`, optional `json`, optional
`params`, and return `mailchannels.SDKResponse`.

```python
from typing import Any

import mailchannels


class LoggingTransport:
    """Small example transport that satisfies SyncHTTPClient."""

    def __init__(self) -> None:
        """Create a logging transport with a pooled inner transport."""
        self._inner = mailchannels.RequestsClient()

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
        return self._inner.request(
            method,
            url,
            headers=headers,
            json=json,
            params=params,
        )

    def close(self) -> None:
        """Close the pooled inner transport."""
        self._inner.close()


client = mailchannels.Client(
    api_key="YOUR-API-KEY",
    http_client=LoggingTransport(),
)
```

Module-level clients can use `mailchannels.default_http_client` and
`mailchannels.default_async_http_client` with any protocol-compatible transport.

## Low-Level Webhook Helpers

MailChannels signs webhooks with Ed25519 and documents the signing flow in terms
of RFC 9421. `Webhooks.verify(...)` performs digest, freshness, and signature
verification when given the public signing key returned by
`Webhooks.public_key(...)`.

`verify_content_digest(...)`, `parse_signature_input(...)`,
`signature_key_id(...)`, and `signature_is_fresh(...)` remain available as
low-level helpers when an application needs to inspect individual checks.

By default, signature timestamps may be up to 300 seconds old and no more than
30 seconds in the future. Pass `max_age_seconds` or `max_skew_seconds` to
`Webhooks.verify(...)` if your receiver needs a different replay window.
