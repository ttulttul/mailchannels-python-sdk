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

Status: implemented. `ResponseValidationError` covers strict response model
failures, `RateLimitError` covers 429 responses, `InvalidRequestError` covers
generic 4xx request failures, and `ServerError` covers 5xx failures. These API
response exceptions inherit from `ApiError` for backward-compatible catch-all
handling.
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

## Enhanced Testing

You’re now past the “basic endpoint coverage” stage. The tests I’d add next are mostly **conformance, parity, and regression-hardening tests**.

## Highest-priority additions

### 1. Bidirectional OpenAPI drift detection

Your current drift script validates that every SDK-declared route exists in the OpenAPI spec. That catches “SDK invented or stale route” bugs, but not “OpenAPI added a new route and the SDK forgot to implement it” bugs. The script currently computes only SDK routes missing from the spec via `_missing_routes(spec_routes)`. ([GitHub][1])

Add tests and script logic for both directions:

```python
sdk_missing_from_spec = SDK_ROUTES - spec_routes
spec_missing_from_sdk = spec_routes - SDK_ROUTES
```

Then allowlist only intentionally unsupported spec paths, if any.

This is the single most important remaining conformance test because your route registry is now central to SDK/API alignment. ([GitHub][2])

Status: implemented. The drift script now compares SDK and OpenAPI routes in both directions and the route snapshot asserts exact equality.

I’d add fixture specs for:

| Case                                       | Expected               |
| ------------------------------------------ | ---------------------- |
| Exact route match                          | pass                   |
| SDK route absent from spec                 | fail                   |
| Spec route absent from SDK                 | fail                   |
| Intentional unsupported route in allowlist | pass                   |
| Invalid OpenAPI YAML                       | fail cleanly           |
| Local `--spec-path`                        | tested without network |

### 2. Request-shape contract tests against OpenAPI schemas

The current OpenAPI contract test is route-level: method/path membership and snapshot length. That is valuable, but it cannot detect wrong request bodies, wrong query names, wrong header placement, or omitted required fields. ([GitHub][3])

Add operation-level contract tests that validate the SDK-generated request against the OpenAPI request schema. For each operation, construct a minimal valid SDK call, intercept the fake transport call, then validate:

| Contract area        | Example                                           |
| -------------------- | ------------------------------------------------- |
| Path                 | `/sub-account/{handle}/limit`                     |
| Method               | `PUT`                                             |
| JSON body            | `{"sends": 100000}`                               |
| Query params         | `dry-run=true`, `limit`, `offset`, `start_time`   |
| Headers              | `X-Api-Key`, `X-Customer-Handle` where applicable |
| No accidental extras | no legacy `monthly_limit` in outgoing JSON        |

This would have caught the earlier plural `/limits` problem and would also catch future subtle shape regressions.

Status: implemented. `tests/test_openapi_request_contract.py` executes every supported SDK operation through the fake transport and validates the generated request method, concrete path, JSON keys, query keys, required headers, forbidden headers, and legacy payload-key exclusions.

### 3. A generated “every route has a call test” matrix

Right now, route coverage is spread across resource-specific tests: DKIM, metrics, sub-accounts, suppressions, usage, webhooks, domain checks, etc. That is readable, but it leaves room for a new route to be added to `SDK_ROUTES` without a concrete request-construction test. ([GitHub][4])

Add a parametrized test table keyed by route operation:

```python
ROUTE_CALLS = {
    ("POST", "/send"): lambda client: client.emails.send(...),
    ("POST", "/send-async"): lambda client: client.emails.queue(...),
    ("POST", "/check-domain"): lambda client: client.check_domain.check("example.com"),
    ...
}
```

Then assert:

```python
assert set(ROUTE_CALLS) == sdk_route_keys()
```

For each route:

```python
call = transport.calls[0]
assert call["method"] == method
assert strip_base_url(call["url"]) == path_with_sample_values
```

This gives you an immediate failure when a developer updates the route registry but forgets to add an executable request test.

Status: implemented. `ROUTE_CONTRACTS` is keyed by SDK method/path and `test_operation_contracts_cover_every_sdk_route` requires the matrix to match `sdk_route_keys()` exactly.

### 4. Sync/async parity tests for every async-capable method

You already test async for representative methods, including emails, DKIM, metrics, sub-accounts, suppressions, usage, webhooks, and domain checks. ([GitHub][5])

The next step is systematic parity: for every sync method with an async counterpart, assert the async call emits the same method, URL, params, JSON, and headers. Resend’s test tree is stronger here because it has many paired sync/async test files across resources. ([GitHub][6])

This is especially useful for SDKs because async methods often drift when features are added quickly.

Status: implemented. `tests/test_openapi_request_contract.py` stores sync and async calls in the same operation contract rows and asserts their fake-transport request dictionaries match exactly.

### 5. HTTP transport tests, not just fake transport tests

Most current tests use fake transports, which is good for unit tests. But the real sync and async transports deserve direct tests too. `RequestsClient` wraps `requests.request`, handles JSON decoding failure, returns `SDKResponse`, and preserves response headers. `HTTPXClient` imports `httpx` lazily, opens an `AsyncClient`, handles JSON decode errors, and raises `AsyncClientNotConfigured` when async dependencies are missing. ([GitHub][7])

Add tests for:

| Transport case                                                     | Why                                          |
| ------------------------------------------------------------------ | -------------------------------------------- |
| `requests.request` receives method/url/headers/json/params/timeout | catches transport signature regressions      |
| Non-JSON response returns `data=None`                              | protects 204 / HTML / plain-text responses   |
| Headers preserved exactly                                          | request ID and retry metadata depend on this |
| Timeout parameter honored                                          | production reliability                       |
| Async transport with mocked `httpx.AsyncClient`                    | catches async request construction bugs      |
| Async import failure                                               | verifies the optional `[async]` extra UX     |

Status: implemented. `tests/test_http_clients.py` now covers real sync and
async transport argument forwarding, configured timeouts, non-JSON response
normalization, header preservation, and missing-`httpx` configuration errors.

### 6. Negative webhook helper tests

Webhook helper tests currently cover a happy-path parse/digest/freshness case. ([GitHub][8]) Add the ugly cases:

| Test                                | Expected          |
| ----------------------------------- | ----------------- |
| Missing `Content-Digest`            | `False`           |
| Wrong digest                        | `False`           |
| Malformed digest                    | `False`           |
| Non-base64 digest                   | no crash; `False` |
| Header case variations              | still works       |
| Missing `Signature-Input`           | `None` key ID     |
| Malformed `Signature-Input`         | `ValueError`      |
| Missing `created`                   | stale / not fresh |
| Created timestamp outside tolerance | `False`           |
| Future timestamp outside tolerance  | `False`           |

These are high-value because webhook verification code usually fails in edge cases, not in the happy path.

Status: implemented. `tests/test_webhooks.py` now covers missing, wrong,
malformed, and non-base64 digests, case-insensitive header lookup, missing and
malformed signature input, missing timestamps, and stale or future timestamps.

### 7. More complete error mapping tests

Current error tests cover 403, 409, 413, 429 metadata, and null-body fallback. ([GitHub][9]) Add the missing direct mappings:

| Status/body                | Expected                                        |
| -------------------------- | ----------------------------------------------- |
| 401                        | `AuthenticationError`                           |
| 400                        | generic `ApiError` with `invalid_request_error` |
| 404                        | generic `ApiError`                              |
| 422                        | generic `ApiError`                              |
| 500                        | generic `ApiError` with `server_error`          |
| 502                        | `BadGatewayError`                               |
| dict body with `error`     | message extracted                               |
| dict body with `detail`    | message extracted                               |
| dict body with `title`     | message extracted                               |
| plain-text body            | text fallback                                   |
| empty body                 | status fallback                                 |
| request ID header variants | all recognized                                  |

The exception class already supports request IDs from multiple header names and stable diagnostic fields, so tests should lock that behavior down. ([GitHub][10])

Status: implemented. `tests/test_errors.py` now covers direct mappings for 400,
401, 404, 422, 500, and 502 responses, structured and plain-text message
extraction, empty-body fallback messages, and request ID header variants.

## Medium-priority additions

### 8. Strict response model coverage for every typed response

You already test strict responses for usage, including validation failure. ([GitHub][11]) Extend that across every response model you expose: usage, domain checks, DKIM, metrics, suppressions, webhooks, and sub-account usage.

For each model:

1. Valid minimal API body parses.
2. Extra fields are handled as intended.
3. Missing required fields fail.
4. Invalid types fail with `ResponseValidationError`.
5. `http_headers` are preserved.

This turns strict response mode into a reliable product feature rather than a partially tested option.

### 9. Email payload negative tests

Your email tests are already good on normalization, templates, custom headers, DKIM fields, attachments, dry-run, async queueing, and module-level config. ([GitHub][5]) Add negative payload tests:

| Case                               | Expected                      |
| ---------------------------------- | ----------------------------- |
| Missing `from`                     | validation error              |
| Missing recipient                  | validation error              |
| Missing subject if API requires it | validation error              |
| No content/text/html               | validation error              |
| Invalid email address shape        | validation error, if enforced |
| Empty attachments list             | normalized cleanly            |
| Attachment file missing            | clear exception               |
| Remote attachment 404              | propagates clear error        |
| URL attachment with no filename    | sensible filename fallback    |
| Conflicting shortcut/native fields | deterministic behavior        |

The goal is to test what developers will get wrong.

### 10. Live online CRUD lifecycle tests, carefully isolated

The online tests now cover usage, async usage, send dry-run, optional real send, metrics volume, sub-account list, suppression list, webhooks list, DKIM list, and live domain checks. ([GitHub][12]) The manual workflow runs these via `workflow_dispatch` and uses environment variables for API key, URL, test sender/recipient, test domain, and real-send opt-in. ([GitHub][13])

Add a separate `online_destructive` or `online_crud` marker for isolated create/update/delete flows:

| Resource       | Suggested live test                                                                                     |
| -------------- | ------------------------------------------------------------------------------------------------------- |
| Suppressions   | create unique recipient, list/filter it, delete it                                                      |
| Sub-accounts   | create unique handle, set limit, retrieve limit, delete limit, suspend/activate if safe, delete account |
| API keys       | create/list/delete under throwaway sub-account                                                          |
| SMTP passwords | create/list/delete under throwaway sub-account                                                          |
| Webhooks       | create test endpoint, validate, list, delete                                                            |
| DKIM           | create/list/update/rotate only on a designated test domain                                              |

Use `try/finally` cleanup and unique names like `sdk-test-{timestamp}`. Keep these separate from routine CI to avoid accidental production mutation.

Status: implemented. `tests/test_online_crud.py` adds destructive lifecycle
tests for suppressions, sub-accounts plus API keys/SMTP passwords/limits, and
webhooks. They are gated behind `online_destructive`,
`--online-destructive`, and `MAILCHANNELS_ONLINE_DESTRUCTIVE=1`.

### 11. Consumer typing tests

The package presents itself as typed, and `pyproject.toml` runs mypy only on `src/mailchannels` and `scripts`. ([GitHub][14]) Add a small `typing_tests/` or `tests/typing/` fixture that simulates a user project:

```python
from mailchannels import Client
from mailchannels.emails import EmailParams, EmailAddress

client = Client(api_key="x")
params = EmailParams(
    from_=EmailAddress(email="sender@example.com"),
    personalizations=[{"to": [{"email": "to@example.com"}]}],
    subject="Hello",
    content=[{"type": "text/plain", "value": "Hi"}],
)
client.emails.queue(params)
```

Then run mypy against that fixture in CI. This catches issues that internal package typing can miss, especially exported aliases and public model names.

Status: implemented. `typing_tests/consumer_project.py` simulates external SDK
usage and `scripts/run_consumer_typing.py` runs it through strict mypy in CI.

### 12. Package installation smoke tests

Add CI jobs that build the wheel, install it into a clean virtual environment, and run import/smoke tests:

| Install mode             | Test                                                |
| ------------------------ | --------------------------------------------------- |
| `pip install dist/*.whl` | `import mailchannels; mailchannels.Client`          |
| without `[async]`        | sync works; async gives helpful missing-extra error |
| with `[async]`           | async client imports and can use mocked transport   |
| wheel metadata           | version, dependencies, `py.typed` included          |

The current CI builds the package, but I do not see an install-from-wheel smoke test. ([GitHub][15])

Status: implemented. `scripts/smoke_wheel_install.py` installs the built wheel
into clean environments, verifies imports and `py.typed`, checks the helpful
missing-async-extra error without `httpx`, and verifies the `[async]` extra.

## Lower-priority but valuable

### 13. Coverage threshold and branch coverage

Resend’s CI uploads coverage; your current CI runs tests, quality checks, build, and OpenAPI drift, but I do not see coverage collection or a threshold. ([GitHub][16])

Add:

```bash
pytest --cov=mailchannels --cov-branch --cov-report=term-missing --cov-fail-under=90
```

The number can start lower and ratchet up. Branch coverage is especially useful for error handling, optional async imports, and webhook helper negatives.

Status: implemented. The dev dependencies include `pytest-cov`, coverage is
configured for branch coverage with an 85% fail-under threshold, and CI runs the
coverage gate on Python 3.13. Current measured branch coverage is 88%.

### 14. CI Python matrix expansion

The package supports Python `>=3.9`; current CI tests Python 3.9 and 3.13. ([GitHub][14]) I’d add 3.10, 3.11, and 3.12. This is not as urgent as contract tests, but it catches dependency and typing edge cases across the supported range.

Status: implemented. CI now runs pytest on Python 3.9, 3.10, 3.11, 3.12, and
3.13.

### 15. README example extraction tests

You already test example files directly, which is excellent. ([GitHub][17]) The next level is extracting fenced Python snippets from `README.md` and smoke-testing them after replacing credentials/transports. That prevents the README from drifting away from executable SDK behavior.

Status: implemented. `tests/test_readme_examples.py` extracts every Python code
fence from `README.md`, compiles all snippets with README line-number IDs, and
executes safe snippets with fake sync and async transports plus temporary sample
files. External integration snippets, such as Cloudflare DNS publishing, are
explicitly skipped for execution while still being syntax-checked.

### 16. Automate PyPI publishing via GitHub Actions

Next up, add a release workflow that builds the package, verifies the wheel,
and publishes to PyPI from GitHub Actions. Prefer PyPI trusted publishing via
OpenID Connect over long-lived API tokens, and gate publication on tags or
manual `workflow_dispatch` so routine pushes to `main` keep running tests
without publishing a release.

Status: implemented. `.github/workflows/publish.yml` builds and verifies the
package, checks tag/version alignment for `v*` tags, uploads the distribution as
an artifact, and publishes through PyPI trusted publishing from the `pypi`
environment.
Priority: high.

## My recommended order

1. **Generate `docs/API_COVERAGE.md`**
2. **Strict response model coverage for every typed response**
3. **Add API spec compatibility guarantees**

This would make MailChannels stronger than Resend not only in SDK design and docs, but also in API-conformance discipline. Resend still has broader raw unit-test volume, especially paired async coverage, but you can leapfrog it by making OpenAPI conformance and route/request parity the backbone of the suite.

[1]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/scripts/check_openapi_drift.py "raw.githubusercontent.com"
[2]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/src/mailchannels/routes.py "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/tests/test_openapi_contract.py "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/tests/test_dkim.py "raw.githubusercontent.com"
[5]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/tests/test_emails.py "raw.githubusercontent.com"
[6]: https://github.com/resend/resend-python/tree/main/tests "resend-python/tests at main · resend/resend-python · GitHub"
[7]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/src/mailchannels/http_client.py "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/tests/test_webhooks.py "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/tests/test_errors.py "raw.githubusercontent.com"
[10]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/src/mailchannels/exceptions.py "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/tests/test_response_config.py "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/tests/test_online_api.py "raw.githubusercontent.com"
[13]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/.github/workflows/online-tests.yml "raw.githubusercontent.com"
[14]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/pyproject.toml "raw.githubusercontent.com"
[15]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/.github/workflows/ci.yml "raw.githubusercontent.com"
[16]: https://raw.githubusercontent.com/resend/resend-python/main/.github/workflows/ci.yaml "raw.githubusercontent.com"
[17]: https://raw.githubusercontent.com/ttulttul/mailchannels-python-sdk/main/tests/test_examples.py "raw.githubusercontent.com"
