# SDK Wishlist

This wishlist is the active roadmap for the MailChannels Python SDK. Completed
items have been removed from the active queue so this file stays useful for
choosing the next engineering task.

## Recommended Order

1. Add API spec compatibility guarantees
2. Add email payload negative tests
3. Generate a formal API reference
4. Explore OpenAPI-assisted generation
5. Add request options if the API exposes per-request controls

## 1. Add API Spec Compatibility Guarantees

Tie SDK releases to the MailChannels OpenAPI document they were checked against.
Expose the OpenAPI source URL, spec hash, and checked date in generated
documentation or package metadata so users can see which API contract a release
targets.

`docs/API_COVERAGE.md` now includes the spec URL, SHA-256 hash, generated
timestamp, and SDK version. The next step is deciding whether to expose this
contract metadata from package metadata or a public module constant for runtime
introspection.

Priority: high.

## 2. Add Email Payload Negative Tests

Email normalization has broad positive coverage for templates, custom headers,
DKIM fields, attachments, dry runs, async queueing, and module-level config. Add
negative tests for common developer mistakes.

Suggested cases:

| Case | Expected |
| --- | --- |
| Missing `from` | Validation error. |
| Missing recipient | Validation error. |
| Missing subject if API requires it | Validation error. |
| No `content`, `text`, or `html` | Validation error. |
| Invalid email address shape | Validation error if enforceable. |
| Empty attachments list | Normalized cleanly. |
| Attachment file missing | Clear exception. |
| Remote attachment 404 | Clear propagated error. |
| URL attachment with no filename | Sensible filename fallback. |
| Conflicting shortcut/native fields | Deterministic documented behavior. |

The goal is to test what developers will actually get wrong before their code
reaches the MailChannels API.

Priority: medium.

## 3. Generate a Formal API Reference

The README is strong as a guide and tutorial, but the project also needs a
formal generated API reference that lists public classes, methods, parameters,
return types, and examples.

A lightweight documentation tool should read type hints and docstrings from
`src/mailchannels` and generate stable reference pages. The generated reference
should complement the README rather than turn the README into exhaustive API
documentation.

Priority: medium.

## 4. Explore OpenAPI-Assisted Generation

Investigate generating selected SDK artifacts from the MailChannels OpenAPI
spec. A fully generated SDK may not be the right product design, but generated
route declarations, operation metadata, request-shape tests, response-model
stubs, or coverage reports could reduce human error while preserving the
hand-written ergonomic SDK surface.

Keep this exploratory until the coverage report and strict response tests make
the desired generated artifacts obvious.

Priority: medium.

## 5. Add Request Options If Needed

If MailChannels exposes per-request option headers such as idempotency keys,
model them as an `options` argument rather than forcing those controls into
payloads.

Do not build this speculatively. Add it only when there is a concrete
MailChannels API need or documented per-request option.

Priority: low.

## Completed Foundation

The following roadmap items are complete and should not be re-added unless the
API changes:

- Sub-account limit conformance to singular `/sub-account/{handle}/limit`.
- `/check-domain` support.
- Route registry and bidirectional OpenAPI drift checks.
- Generated `docs/API_COVERAGE.md` endpoint coverage report.
- Operation-level request contract tests.
- Exact route-call matrix coverage.
- Sync/async request parity tests.
- Strict response mode and initial typed response models.
- Strict response model coverage across the modeled SDK response surface.
- Refined API error taxonomy.
- HTTP transport edge-case tests.
- Webhook negative helper tests.
- Manual online and destructive online test workflows.
- Consumer typing tests.
- Wheel install smoke tests.
- Coverage tooling and Python CI matrix expansion.
- README Python snippet extraction tests.
- PyPI publishing workflow.
- Focused examples for templates, unsubscribe, custom headers, DKIM,
  Cloudflare DKIM publication, sub-accounts, metrics, and existing operational
  examples.
