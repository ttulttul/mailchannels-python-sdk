# Development

This project uses uv for Python package management. Run the full local checks
before committing changes:

```bash
uv sync --extra async --extra dev
uv run pytest
uv run pytest --cov --cov-report=term-missing
uv run ruff check src tests examples scripts typing_tests
uv run mypy
uv run python scripts/run_consumer_typing.py
uv build
uv run python scripts/smoke_wheel_install.py
uv run python scripts/check_openapi_drift.py
uv run python scripts/generate_api_coverage.py
uv run python scripts/generate_api_reference.py
```

Current uv releases do not expose `uv pytest` as a native subcommand; use
`uv run pytest` for the portable pytest harness.

## CI

The GitHub Actions CI workflow runs checks on pushes to `main`, pull requests,
and manual dispatches. It runs pytest across Python 3.9 through 3.13 and
enforces an 85% branch coverage threshold on Python 3.13. It also compares the
SDK's declared routes with the official MailChannels OpenAPI spec so documented
endpoint changes are caught early.

The unit test suite includes direct transport-wrapper tests, explicit API error
mapping tests, strict response model validation, negative email payload tests,
README snippet smoke tests, external-consumer type checks, and clean wheel
install checks with and without the `[async]` extra.

The separate online API workflow is manual-only and expects
`MAILCHANNELS_API_KEY` as a GitHub secret plus optional repository or
environment variables for sender, recipient, DKIM domain, and API URL.

## Publishing

The PyPI publishing workflow builds, tests, type-checks, validates OpenAPI
drift, runs `twine check`, and publishes the verified `dist/` artifact through
PyPI trusted publishing.

Configure PyPI with a trusted publisher for `.github/workflows/publish.yml` and
the GitHub environment `pypi`. Push a version tag such as `v0.1.0`, matching
`pyproject.toml`, to publish automatically, or run the workflow manually with
`publish=true`.

## Online API Tests

The default test suite never calls the live MailChannels API. Online tests are
marked with `online` and run only when you both provide a real API key in the
environment and pass `--online`.

```bash
export MAILCHANNELS_API_KEY="your_real_mailchannels_api_key"
uv run pytest -m online --online
```

The online suite includes parent-account usage, async usage, volume metrics,
sub-account listing, suppression listing, webhook listing, optional domain
checks, DKIM listing, dry-run sending, and dry-run rejection checks for
malformed raw send payloads. The volume metrics test sends an explicit 24-hour
`start_time` and `end_time` window so the live service does not need to infer an
unbounded range. The send tests use MailChannels dry runs, which do not deliver
messages. Set sender and recipient addresses to enable those dry-run tests:

```bash
export MAILCHANNELS_ONLINE_FROM="sender@example.com"
export MAILCHANNELS_ONLINE_TO="recipient@example.net"
uv run pytest -m online --online
```

To run the optional `/check-domain` and DKIM listing tests, provide a domain
that belongs to the account:

```bash
export MAILCHANNELS_ONLINE_DOMAIN="example.com"
uv run pytest -m online --online
```

The suite also includes a test that sends a real email through `/send`. It is
disabled unless you explicitly opt in with `MAILCHANNELS_ONLINE_SEND_REAL=1`:

```bash
export MAILCHANNELS_ONLINE_FROM="sender@example.com"
export MAILCHANNELS_ONLINE_TO="recipient@example.net"
export MAILCHANNELS_ONLINE_SEND_REAL=1
uv run pytest tests/test_online_api.py::test_online_send_real_email --online
```

Use `MAILCHANNELS_API_URL` if you need to point the online tests at a non-default
MailChannels API host.

If the live MailChannels service returns a 5xx response, times out, or drops a
connection for an online endpoint, that test is reported as `xfail` because the
failure is outside the local SDK behavior being tested. Authentication and
authorization errors still fail the test normally.

Destructive online CRUD tests are marked `online_destructive` and stay disabled
unless you pass both `--online` and `--online-destructive` and set
`MAILCHANNELS_ONLINE_DESTRUCTIVE=1`. Run these only against a dedicated test
account because they create and delete suppressions, sub-accounts, credentials,
limits, and webhook configuration. The MailChannels webhook delete endpoint
removes all configured webhooks.

```bash
export MAILCHANNELS_ONLINE_DESTRUCTIVE=1
uv run pytest -m online_destructive --online --online-destructive
```

## SmolVM Verification

Run the suite in SmolVM before committing. In this macOS sandbox, copying a tar
archive into the VM is more reliable than a direct bind mount:

```bash
COPYFILE_DISABLE=1 tar --exclude .venv --exclude .git --exclude dist --exclude .mypy_cache --exclude .ruff_cache --exclude .pytest_cache -cf /tmp/mailchannels-python-sdk.tar .
smolvm machine create mc-sdk-tests --net --image python:3.13-slim
smolvm machine start --name mc-sdk-tests
smolvm machine cp /tmp/mailchannels-python-sdk.tar mc-sdk-tests:/workspace/mailchannels-python-sdk.tar
smolvm machine exec --name mc-sdk-tests -- sh -lc 'cd /workspace && mkdir -p mailchannels-python-sdk && tar -xf mailchannels-python-sdk.tar -C mailchannels-python-sdk && cd mailchannels-python-sdk && pip install uv && uv sync --extra async --extra dev && uv run pytest'
smolvm machine stop --name mc-sdk-tests
```
