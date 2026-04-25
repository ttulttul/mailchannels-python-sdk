# SDK Wishlist

This wishlist is the current product and engineering roadmap for the
MailChannels Python SDK. Earlier Resend-alignment work has mostly landed; the
next phase should focus on API conformance, drift detection, stronger response
typing, and formal documentation coverage.

## 1. Fix Sub-Account Limit API Conformance

The SDK previously modeled sub-account limits with
`/sub-account/{handle}/limits` and `POST` for setting limits. The official
MailChannels documentation specifies `PUT /sub-account/:handle/limit` with a
singular `limit` path. Existing retrieval and deletion paths also needed to be
checked and corrected to the documented singular endpoint.

Status: implemented. The SDK now uses `PUT`, `GET`, and `DELETE` against
`/sub-account/{handle}/limit` and sends the documented `{"sends": ...}` payload
when setting limits.
Priority: high.

## 2. Implement `/check-domain`

Add support for `POST /check-domain`, which checks DKIM, SPF, and Domain
Lockdown status. This should include sync and async client-bound methods,
module-level helpers if consistent with the rest of the SDK, typed request
models where useful, tests, README coverage, and a focused example if the
endpoint has enough setup nuance.

Status: implemented. The SDK exposes `client.domain_checks.check()`,
`client.domain_checks.check_async()`, `mailchannels.DomainChecks.check()`, and
`mailchannels.DomainChecks.check_async()` for `/check-domain`.
Priority: high.

## 3. Add API-Contract Tests

The test suite should validate SDK routes, paths, and methods against the
official MailChannels OpenAPI specification or an equivalent live sandbox
contract. This is especially important because the current tests can reinforce
incorrect SDK behavior when they only assert internal request construction.

Status: implemented. The SDK has a route registry and a drift checker that
compares supported route declarations with the official OpenAPI spec.
Priority: high.

## 4. Add OpenAPI Drift CI

Add an automated CI job that compares the SDK's declared routes and methods with
the official MailChannels OpenAPI spec. The goal is not necessarily to generate
the whole SDK immediately, but to fail fast when a hand-written resource drifts
from documented API paths, methods, or required parameters.

Status: implemented. CI runs `scripts/check_openapi_drift.py` as a separate
OpenAPI drift job.
Priority: high.

## 5. Rewrite Sub-Account Limit Tests

Update existing sub-account tests so they assert the correct singular
`/sub-account/{handle}/limit` endpoint and the documented HTTP method. These
tests should fail if the SDK regresses to `/limits` or uses the wrong method.

Status: implemented. Sub-account tests now assert singular `/limit`, `PUT` for
setting limits, and the documented `sends` request payload.
Priority: high.

## 6. Return Strongly Typed Responses

The SDK has strong Pydantic validation for incoming request payloads, but most
operations return dict-like response wrappers. Introduce strongly typed response
objects where the API has stable response shapes, while preserving ergonomic
dict-style and attribute-style access for callers who prefer lightweight usage.

Status: implemented. The client now accepts `strict_responses=True`, endpoint
resources pass response models for stable API shapes, and strict mode returns
validated Pydantic response objects while the default mode keeps dict-like
responses.
Priority: high.

## 7. Generate OpenAPI Coverage Reports

Generate `docs/API_COVERAGE.md` from the official OpenAPI spec and the SDK route
registry. The first report should expose endpoint coverage. Later iterations
should add request-field and response-field coverage as request and response
models become more complete.

Status: pending.
Priority: high.

## 8. Refine Error Taxonomy

The SDK already preserves structured error metadata, request IDs, retry hints,
headers, parsed responses, and common typed exceptions. Add narrower exception
classes for rate limits, invalid requests, server errors, and strict response
validation so callers can handle these cases without inspecting `error_type`.

Status: partial. `ResponseValidationError` is implemented for strict response
model failures; rate-limit and generic invalid/server errors still need explicit
subclasses.
Priority: high.

## 9. Add API Spec Compatibility Guarantees

Tie SDK releases to the MailChannels OpenAPI document they were checked
against. Expose the OpenAPI source URL, spec hash, and checked date in generated
documentation or package metadata so users can see which API contract a release
targets.

Status: pending.
Priority: medium.

## 10. Explore OpenAPI Generation

Investigate generating core route declarations, response models, or request
models from the MailChannels OpenAPI spec. A full generated SDK may not be the
right design, but generated routing metadata or model tests would reduce human
error while preserving the hand-written ergonomics that make this SDK pleasant
to use.

Status: pending.
Priority: medium.

## 11. Add an OpenAPI Coverage Matrix

Create a documentation matrix that maps MailChannels OpenAPI endpoints to SDK
support. Each row should include method, path, SDK resource/method, sync support,
async support, test coverage, online-test coverage where applicable, and status
such as supported, partial, pending, or intentionally omitted.

Status: pending.
Priority: medium.

## 12. Generate an API Reference

The README is strong as a guide and tutorial, but the project also needs a
formal generated API reference that lists public classes, methods, parameters,
return types, and examples. This could be built with a lightweight documentation
tool that reads type hints and docstrings from `src/mailchannels`.

Status: pending.
Priority: medium.

## 13. Complete Focused Example Coverage

The repository has tested examples for async sending, attachments,
suppressions, webhooks, usage, custom HTTP clients, and structured error
handling. Add or verify focused examples for templates, unsubscribe, custom
headers, DKIM, Cloudflare DKIM publication, sub-accounts, and metrics.

Status: pending.
Priority: medium.

## 14. Request Options

If MailChannels exposes per-request option headers such as idempotency keys,
model them as an `options` argument rather than forcing those controls into
payloads. Keep this low priority until there is a concrete MailChannels API need.

Status: pending.
Priority: low.

## Completed Foundation Work

The following Resend-alignment and SDK-foundation items are already implemented:
environment variable configuration, response headers, attribute-style response
access, async parity across resources, webhooks, suppressions, top-level usage,
pagination helpers, attachment ergonomics, version export, formal custom HTTP
client protocols, better exception metadata, CI, type checking, and manual
online-test workflows.
