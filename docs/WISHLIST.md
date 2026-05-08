# SDK Wishlist

This wishlist is the active roadmap for the MailChannels Python SDK. Completed
items have been removed from the active queue so this file stays useful for
choosing the next engineering task.

## Recommended Order

1. Lower intentional destructive-operation logs from warning to info
2. Add API spec compatibility guarantees
3. Explore OpenAPI-assisted generation
4. Add request options if the API exposes per-request controls

## 1. Lower Intentional Destructive-Operation Logs

User-initiated destructive calls currently log at warning level in DKIM,
webhooks, sub-accounts, and suppressions. Lower those normal operations to info
level and reserve warning for unexpected recoverable behavior.

Priority: high.

## 2. Add API Spec Compatibility Guarantees

Tie SDK releases to the MailChannels OpenAPI document they were checked against.
Expose the OpenAPI source URL, spec hash, and checked date in generated
documentation or package metadata so users can see which API contract a release
targets.

`docs/API_COVERAGE.md` now includes the spec URL, SHA-256 hash, generated
timestamp, and SDK version. The next step is deciding whether to expose this
contract metadata from package metadata or a public module constant for runtime
introspection.

Priority: high.

## 3. Explore OpenAPI-Assisted Generation

Investigate generating selected SDK artifacts from the MailChannels OpenAPI
spec. A fully generated SDK may not be the right product design, but generated
route declarations, operation metadata, request-shape tests, response-model
stubs, or coverage reports could reduce human error while preserving the
hand-written ergonomic SDK surface.

Keep this exploratory until the coverage report and strict response tests make
the desired generated artifacts obvious.

Priority: medium.

## 4. Add Request Options If Needed

If MailChannels exposes per-request option headers such as idempotency keys,
model them as an `options` argument rather than forcing those controls into
payloads.

Do not build this speculatively. Add it only when there is a concrete
MailChannels API need or documented per-request option.

Priority: low.

## Other Cleanup Candidates

- Remove or handle dead branches in `raise_for_status` for 1xx and 3xx
  responses.
- Split SDK payload validation errors from Pydantic validation errors with a
  more specific exception or richer error details.
- Document that `Webhooks.resend_batch` is unauthenticated and identified only
  by `X-Customer-Handle`.
- Simplify `limit_payload` dead paths and make the `monthly_limit` alias
  decision explicit.
- Add an async attachment fetch helper or document that `Attachment.from_url`
  blocks the event loop.
- Reduce sender alias sprawl by documenting `from_` as canonical and treating
  the other aliases as compatibility paths.
- Rename underscore-prefixed sub-account proxy classes or hide them behind a
  clearer namespace.
- Preserve typing in `Suppressions.list(**kwargs)`.
- Decide whether the US-spelling metrics alias should be unique or part of a
  broader spelling-compatibility policy.
- Audit metrics response fields so required-vs-optional strict parsing is
  intentional.

## Completed Foundation

The following roadmap items are complete and should not be re-added unless the
API changes:

- Sub-account limit conformance to singular `/sub-account/{handle}/limit`.
- `/check-domain` support.
- Route registry and bidirectional OpenAPI drift checks.
- Generated `docs/API_COVERAGE.md` endpoint coverage report.
- Generated `docs/API_REFERENCE.md` public SDK reference.
- Operation-level request contract tests.
- Exact route-call matrix coverage.
- Sync/async request parity tests.
- Strict response mode and initial typed response models.
- Strict response model coverage across the modeled SDK response surface.
- Strict `/send` and `/send-async` response variant validation.
- Strict response return typing for explicit `Client(strict_responses=True)`
  callers across the modeled resource surface.
- Persistent sync and async HTTP transport client pooling with explicit close
  and context-manager lifecycle hooks.
- Directional webhook signature freshness checks with separate stale-age and
  future-skew windows.
- Full webhook digest, freshness, and RFC 9421 Ed25519 signature verification.
- Email payload negative tests for local validation, mocked API rejection, and
  live dry-run API rejection.
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
