# SDK Wishlist

This wishlist compares the MailChannels Python SDK with the local
`../resend-python` SDK from an SDK ergonomics point of view. It does not assume
MailChannels should copy Resend's API surface; it identifies reusable SDK
features and support patterns that would make this package feel more complete.

## 1. Environment Variable Configuration

Resend auto-loads its API key and API URL from environment variables. The
MailChannels SDK should support `MAILCHANNELS_API_KEY` and
`MAILCHANNELS_API_URL` so scripts and deployed services can be configured
without assigning module globals in code.

Status: implemented.
Priority: high.

## 2. Response Headers

Resend preserves HTTP response headers in API responses. MailChannels responses
should expose `http_headers` so callers can inspect request IDs, rate-limit
headers, retry hints, and diagnostic metadata.

Status: implemented.
Priority: high.

## 3. Attribute-Style Response Access

Resend responses can be read as dictionaries or with attribute access. The
MailChannels SDK should return a dict-like response wrapper so both
`response["request_id"]` and `response.request_id` work.

Status: implemented.
Priority: medium.

## 4. Async Parity

Resend provides async variants broadly across resources. MailChannels should
provide `_async` methods for every resource that performs network I/O, not just
email sending.

Status: implemented. Email, DKIM, metrics, sub-account, webhook, and suppression
resources all expose async methods for network I/O.
Priority: high.

## 5. Webhook Resource And Verification Helpers

Resend has webhook management and local verification helpers. MailChannels has
webhook enrollment, deletion, validation, batch listing, batch resend, and
public-key retrieval endpoints. The SDK should expose these as a typed
`Webhooks` resource. If MailChannels webhook signatures can be verified locally
from the documented public-key model, add a verification helper as a follow-up.

Status: implemented. The SDK includes webhook API operations plus helpers for
Signature-Input parsing, key ID extraction, replay-age checks, and
Content-Digest verification. Full Ed25519 verification remains intentionally
delegated to a dedicated HTTP-signature library.
Priority: high.

## 6. Suppression List Resource

Resend has recipient-management resources such as contacts and audiences.
MailChannels' closest equivalent is suppression-list management. The SDK should
support listing, creating, and deleting suppression entries.

Status: implemented.
Priority: high.

## 7. Top-Level Usage Resource

The SDK supports sub-account usage, but not parent-account `/usage`. Add a
top-level `Usage` resource or `Client.usage.retrieve()`.

Status: implemented. The SDK exposes `client.usage.retrieve()`,
`client.usage.retrieve_async()`, `mailchannels.Usage.retrieve()`, and
`mailchannels.Usage.retrieve_async()` for `/usage`.
Priority: medium.

## 8. Pagination Helper

Resend has a shared pagination/query helper. MailChannels currently builds query
parameters resource by resource. Add a small shared query helper for list
endpoints and date serialization.

Status: implemented. The SDK has shared `compact_query()` and
`pagination_query()` helpers used by paginated DKIM, sub-account, suppression,
webhook, and metrics query builders.
Priority: medium.

## 9. Attachment Ergonomics

Resend has examples and types for local, base64, remote, and inline
attachments. MailChannels supports raw attachment fields but lacks helpers for
reading files, Base64 encoding, MIME type inference, and inline `content_id`
examples.

Status: implemented. The SDK exposes `Attachment.from_file()`,
`Attachment.from_bytes()`, `Attachment.from_url()`, and
`Attachment.inline_file()` for Base64 encoding, MIME type inference, filename
overrides, remote content, and inline `content_id` attachments.
Priority: high.

## 10. Version Export

Resend exposes `__version__` and `get_version()`. MailChannels should expose the
same kind of version metadata and use it in the User-Agent.

Status: implemented. The SDK exports `mailchannels.__version__`,
`mailchannels.get_version()`, and uses the exported value in the User-Agent.
Priority: medium.

## 11. Formal Custom HTTP Client Contract

Resend defines HTTP client interfaces and tests custom-client behavior. The
MailChannels SDK accepts transport-like objects but does not expose a formal
`Protocol` or ABC for sync and async clients.

Status: implemented. The SDK exports `SyncHTTPClient` and `AsyncHTTPClient`
protocols and accepts protocol-compatible custom transports both on explicit
clients and through module-level default client configuration.
Priority: medium.

## 12. Better Exception Metadata

Resend exceptions include code, error type, suggested action, and headers.
MailChannels exceptions include status, code, and response. Add headers and
possibly suggested actions for common failures.

Status: implemented. SDK exceptions include response headers, request ID,
retry-after, error type, suggested action, and `to_dict()` metadata for logging.
Priority: medium.

## 13. Example Coverage

Resend has many focused examples. MailChannels should add examples for async,
templates, unsubscribe, custom headers, DKIM, Cloudflare DNS publication,
sub-accounts, metrics, webhooks, suppressions, custom HTTP clients, and errors.

Status: implemented. The repository includes tested examples for async sending,
attachments, suppressions, webhooks, usage, custom HTTP clients, and structured
error handling.
Priority: medium.

## 14. Request Options

Resend supports request options such as idempotency keys where its API supports
them. If MailChannels adds per-request option headers, the SDK should model an
`options` argument rather than forcing those controls into payloads.

Status: pending.
Priority: low.

## 15. CI And Type Checking

Resend has CI, type-checking configuration, and broader test automation.
MailChannels has pytest, ruff, and SmolVM instructions, but no committed GitHub
Actions workflow or static type-check job.

Status: pending.
Priority: low.
