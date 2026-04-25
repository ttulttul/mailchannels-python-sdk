# SDK Wishlist

This wishlist is the current product and engineering roadmap for the
MailChannels Python SDK. Earlier Resend-alignment work has mostly landed; the
next phase should focus on API conformance, drift detection, stronger response
typing, and formal documentation coverage.

## 1. Fix Sub-Account Limit API Conformance

The SDK currently models sub-account limits with `/sub-account/{handle}/limits`
and `POST` for setting limits. The official MailChannels documentation specifies
`PUT /sub-account/:handle/limit` with a singular `limit` path. Existing
retrieval and deletion paths should also be checked and corrected to the
documented singular endpoint.

Status: pending.
Priority: high.

## 2. Implement `/check-domain`

Add support for `POST /check-domain`, which checks DKIM, SPF, and Domain
Lockdown status. This should include sync and async client-bound methods,
module-level helpers if consistent with the rest of the SDK, typed request
models where useful, tests, README coverage, and a focused example if the
endpoint has enough setup nuance.

Status: pending.
Priority: high.

## 3. Add API-Contract Tests

The test suite should validate SDK routes, paths, and methods against the
official MailChannels OpenAPI specification or an equivalent live sandbox
contract. This is especially important because the current tests can reinforce
incorrect SDK behavior when they only assert internal request construction.

Status: pending.
Priority: high.

## 4. Add OpenAPI Drift CI

Add an automated CI job that compares the SDK's declared routes and methods with
the official MailChannels OpenAPI spec. The goal is not necessarily to generate
the whole SDK immediately, but to fail fast when a hand-written resource drifts
from documented API paths, methods, or required parameters.

Status: pending.
Priority: high.

## 5. Rewrite Sub-Account Limit Tests

Update existing sub-account tests so they assert the correct singular
`/sub-account/{handle}/limit` endpoint and the documented HTTP method. These
tests should fail if the SDK regresses to `/limits` or uses the wrong method.

Status: pending.
Priority: high.

## 6. Return Strongly Typed Responses

The SDK has strong Pydantic validation for incoming request payloads, but most
operations return dict-like response wrappers. Introduce strongly typed response
objects where the API has stable response shapes, while preserving ergonomic
dict-style and attribute-style access for callers who prefer lightweight usage.

Status: pending.
Priority: medium.

## 7. Explore OpenAPI Generation

Investigate generating core route declarations, response models, or request
models from the MailChannels OpenAPI spec. A full generated SDK may not be the
right design, but generated routing metadata or model tests would reduce human
error while preserving the hand-written ergonomics that make this SDK pleasant
to use.

Status: pending.
Priority: medium.

## 8. Add an OpenAPI Coverage Matrix

Create a documentation matrix that maps MailChannels OpenAPI endpoints to SDK
support. Each row should include method, path, SDK resource/method, sync support,
async support, test coverage, online-test coverage where applicable, and status
such as supported, partial, pending, or intentionally omitted.

Status: pending.
Priority: medium.

## 9. Generate an API Reference

The README is strong as a guide and tutorial, but the project also needs a
formal generated API reference that lists public classes, methods, parameters,
return types, and examples. This could be built with a lightweight documentation
tool that reads type hints and docstrings from `src/mailchannels`.

Status: pending.
Priority: medium.

## 10. Complete Focused Example Coverage

The repository has tested examples for async sending, attachments,
suppressions, webhooks, usage, custom HTTP clients, and structured error
handling. Add or verify focused examples for templates, unsubscribe, custom
headers, DKIM, Cloudflare DKIM publication, sub-accounts, and metrics.

Status: pending.
Priority: medium.

## 11. Request Options

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
