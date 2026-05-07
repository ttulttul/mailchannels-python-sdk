# SDK Wishlist

This wishlist is the active roadmap for the MailChannels Python SDK. Completed
items have been removed from the active queue so this file stays useful for
choosing the next engineering task.

## Recommended Order

1. Tighten strict response typing and `/send` response validation
2. Reuse HTTP transport clients across requests
3. Add complete webhook signature verification
4. Fix future-dated webhook signature freshness checks
5. Lower intentional destructive-operation logs from warning to info
6. Add API spec compatibility guarantees
7. Explore OpenAPI-assisted generation
8. Add request options if the API exposes per-request controls

## 1. Tighten Strict Response Typing And `/send` Validation

Strict response mode currently returns Pydantic models at runtime while public
resource annotations still say `dict[str, Any]`. That hides the benefit from
type checkers. Add overloads or another typed response strategy so callers who
opt into `strict_responses=True` can see model attributes statically.

The `/send` and `/send-async` response models must also declare the documented
fields instead of accepting any object. Model the normal `/send` request ID and
per-personalization results, the dry-run rendered-message response, and the
`/send-async` request ID and queue timestamp so strict mode detects API drift on
the SDK's highest-volume endpoints.

Priority: high.

## 2. Reuse HTTP Transport Clients Across Requests

The sync transport currently calls `requests.request(...)` directly and the
async transport constructs a new `httpx.AsyncClient` per call. Hold one
`requests.Session` per sync transport and one `httpx.AsyncClient` per async
transport so the SDK gets connection pooling, TLS reuse, and HTTP/2
multiplexing where available. Add close/context-manager support for the async
client and update test fakes accordingly.

Priority: high.

## 3. Add Complete Webhook Signature Verification

`Webhooks.verify_content_digest(...)` only validates the `Content-Digest` header
against the raw body. It does not verify the RFC 9421 Ed25519 signature. Add a
high-level `Webhooks.verify(headers, body, public_key)` helper that verifies the
signature and keep the digest helper as a lower-level primitive with clear
documentation.

Priority: high.

## 4. Fix Future-Dated Webhook Signature Freshness

`signature_is_fresh(...)` uses `abs(reference - created)`, which treats
signatures from the future the same as old signatures. Split the check into
`max_age_seconds` and `max_skew_seconds`, keeping any compatibility alias needed
for one release.

Priority: high.

## 5. Lower Intentional Destructive-Operation Logs

User-initiated destructive calls currently log at warning level in DKIM,
webhooks, sub-accounts, and suppressions. Lower those normal operations to info
level and reserve warning for unexpected recoverable behavior.

Priority: high.

## 6. Add API Spec Compatibility Guarantees

Tie SDK releases to the MailChannels OpenAPI document they were checked against.
Expose the OpenAPI source URL, spec hash, and checked date in generated
documentation or package metadata so users can see which API contract a release
targets.

`docs/API_COVERAGE.md` now includes the spec URL, SHA-256 hash, generated
timestamp, and SDK version. The next step is deciding whether to expose this
contract metadata from package metadata or a public module constant for runtime
introspection.

Priority: high.

## 7. Explore OpenAPI-Assisted Generation

Investigate generating selected SDK artifacts from the MailChannels OpenAPI
spec. A fully generated SDK may not be the right product design, but generated
route declarations, operation metadata, request-shape tests, response-model
stubs, or coverage reports could reduce human error while preserving the
hand-written ergonomic SDK surface.

Keep this exploratory until the coverage report and strict response tests make
the desired generated artifacts obvious.

Priority: medium.

## 8. Add Request Options If Needed

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
