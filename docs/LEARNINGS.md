# Learnings

## 2026-04-24: SDK starts as a greenfield package

The repository currently contains only project instructions, so the SDK can be
structured from first principles around MailChannels Email API behavior rather
than preserving an existing implementation. The first implementation should make
`/send-async` and sub-account operations first-class because those are
MailChannels-specific differentiators rather than secondary endpoints.

## 2026-04-24: uv pytest is not a native uv command

The current uv CLI rejects `uv pytest` as an unknown subcommand. The SDK uses
the portable pytest harness `uv run pytest` instead. SmolVM tests can run by
copying a tar archive of the working tree into a Python VM because direct
SmolVM bind mounts appeared empty in this macOS sandbox.

## 2026-04-24: Templates and unsubscribe are send payload fields

MailChannels templates and unsubscribe behavior are not separate CRUD resources.
Templates are expressed through `content[].template_type = "mustache"` and
`personalizations[].dynamic_template_data`. Unsubscribe links use the
`{{mc-unsubscribe-url}}` mustache placeholder, while automatic
List-Unsubscribe headers are enabled by setting the root send field
`transactional` to `false`. MailChannels documents that List-Unsubscribe also
requires one recipient per personalization and DKIM signing.

## 2026-04-24: Metrics are GET resources under /metrics

The Metrics API has five documented endpoint categories: engagement,
performance, recipient behaviour, volume, and sender metrics. Time-series
endpoints share `start_time`, `end_time`, `campaign_id`, and `interval` query
parameters. Sender metrics use `/metrics/senders/{sender_type}` where
`sender_type` is `campaigns` or `sub-accounts`, with `limit`, `offset`, and
`sort_order` query parameters.

## 2026-04-24: Custom headers are send payload fields

MailChannels custom email headers are expressed through the `headers` object in
the send payload. The same `headers` field is valid inside each personalization
for recipient-specific headers. If the same header exists in both places,
MailChannels uses the personalization-level value.

## 2026-04-24: DKIM has both key-management and send-payload support

MailChannels supports customer-managed DKIM private keys in send payloads and
MailChannels-hosted private keys through `/domains/{domain}/dkim-keys`.
MailChannels returns suggested DKIM DNS records from key-management endpoints,
but the customer must still publish the public DKIM TXT record in their own DNS
zone because MailChannels does not host public DKIM records for customer
domains yet.

## 2026-04-24: Resend comparison highlights SDK ergonomics

The local `../resend-python` comparison produced SDK-level improvements rather
than MailChannels API changes: environment variable configuration, response
headers, attribute-style responses, async parity, webhook resources, and
suppression-list resources are all valuable alignment points. MailChannels
webhooks are signed with `Content-Digest`, `Signature-Input`, and `Signature`;
the SDK can safely provide digest and metadata helpers while leaving final
RFC 9421 Ed25519 verification to a dedicated HTTP-signature library.

## 2026-04-24: Parent usage and pagination share common query helpers

MailChannels exposes both parent-account `/usage` and sub-account
`/sub-account/{handle}/usage`; the SDK now models the parent endpoint as
`Usage` while keeping sub-account usage under `SubAccounts`. Paginated endpoints
share `compact_query()` and `pagination_query()` so date serialization,
comma-separated list serialization, and `limit`/`offset` handling do not drift
between resources.

## 2026-04-24: Attachment ergonomics are local payload helpers

MailChannels attachments are still ordinary send-payload fields, but the SDK can
make them much easier to construct. `Attachment.from_file()`,
`Attachment.from_bytes()`, `Attachment.from_url()`, and
`Attachment.inline_file()` keep Base64 encoding, remote retrieval, MIME
inference, inline disposition, and `content_id` handling close to the attachment
model without adding an API resource that MailChannels does not have.

## 2026-04-24: Version and transports are now explicit SDK contracts

The SDK exports `__version__` and `get_version()` and derives the User-Agent
from that version value, so future releases only need one version source.
Custom HTTP clients are modeled as `SyncHTTPClient` and `AsyncHTTPClient`
protocols returning `SDKResponse`; module-level `default_http_client` and
`default_async_http_client` now accept protocol-compatible transports instead
of only the built-in requests/httpx wrapper classes.

## 2026-04-24: Examples should be importable and tested

The SDK examples now expose small functions for async sending, attachments,
suppressions, webhooks, usage, custom HTTP clients, and structured error
handling. This keeps examples useful as documentation while allowing tests to
exercise them with fake transports and no real network calls.

## 2026-04-24: Exceptions carry support-ready metadata

MailChannels errors now preserve response headers and derive request IDs,
retry-after hints, error types, suggested actions, and `to_dict()` metadata.
This makes example error handling and production logging more useful without
forcing callers to parse raw HTTP responses.

## 2026-04-24: Online tests are explicit and non-delivering by default

Live MailChannels API tests use the `online` pytest marker, require a real
`MAILCHANNELS_API_KEY`, and also require the `--online` flag so local test runs
do not accidentally call production APIs. Online send validation uses
`dry_run=True` and only runs when `MAILCHANNELS_ONLINE_FROM` and
`MAILCHANNELS_ONLINE_TO` are set.

## 2026-04-24: Live API 5xx responses should not look like SDK regressions

The live `/usage` endpoint can return HTTP 500 with a JSON `null` body. Online
tests now report live MailChannels 5xx responses as `xfail`, while preserving
normal failures for 4xx/auth/validation issues. The SDK also avoids surfacing
`null` as an exception message and falls back to a status-based message instead.
Live endpoint timeouts are also external service conditions for online tests,
so they are reported as `xfail` rather than SDK regressions.

## 2026-04-25: Real-send online tests need a second explicit opt-in

Online tests now cover more live read-only endpoints plus dry-run sending. The
test that actually sends an email is intentionally gated behind
`MAILCHANNELS_ONLINE_SEND_REAL=1`, in addition to `MAILCHANNELS_API_KEY`,
`MAILCHANNELS_ONLINE_FROM`, `MAILCHANNELS_ONLINE_TO`, and `--online`, so broad
online test runs do not deliver mail accidentally.

## 2026-04-25: Online metrics tests should use bounded windows

The live `/metrics/volume?interval=day` query can time out when no time range is
provided. The online volume metrics test now sends an explicit recent 24-hour
UTC `start_time` and `end_time` range so it still exercises the endpoint without
depending on the service to infer an unbounded query window. MailChannels bug
`CLOUD-5801` tracks the timeout issue in the metrics API.

## 2026-04-25: CI mirrors local quality gates

The repository now has a GitHub Actions CI workflow that runs pytest on Python
3.9 and 3.13, plus ruff, mypy, and package builds on Python 3.13. Live API tests
belong in a separate manual-only workflow because they require a real
MailChannels API key and may optionally deliver a real email.

## 2026-04-25: SmolVM archives should exclude local tool caches

After adding mypy, the local archive used for SmolVM verification ballooned when
it included `.mypy_cache` and other tool caches, which made VM extraction noisy
and slow. Build SmolVM tarballs with `COPYFILE_DISABLE=1` and exclude `.venv`,
`.git`, `dist`, `.mypy_cache`, `.ruff_cache`, and `.pytest_cache`.

## 2026-04-25: GitHub Actions should use Node 24-ready actions

GitHub CI warned that Node.js 20 actions are deprecated. The workflows now use
`actions/checkout@v6`, `actions/setup-python@v6`, and
`astral-sh/setup-uv@v8.1.0`, which declare the Node 24 runtime and avoid the
deprecation warning without adding a temporary compatibility environment flag.
