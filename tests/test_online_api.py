"""Online tests for the live MailChannels Email API."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import pytest
import requests

import mailchannels

pytestmark = pytest.mark.online


def _client() -> mailchannels.Client:
    """Create a live MailChannels client from environment configuration."""
    return mailchannels.Client(
        api_key=os.environ["MAILCHANNELS_API_KEY"],
        base_url=os.environ.get("MAILCHANNELS_API_URL"),
    )


def test_online_usage_retrieve() -> None:
    """Retrieve parent-account usage from the live API."""
    try:
        result = _client().usage.retrieve()
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except requests.RequestException as error:
        _xfail_live_transport_error(error)
        raise

    assert "http_headers" in result
    assert isinstance(result.http_headers, dict)
    assert "total_usage" in result


async def test_online_usage_retrieve_async() -> None:
    """Retrieve parent-account usage from the live API using async HTTP."""
    try:
        result = await _client().usage.retrieve_async()
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except _httpx_http_error() as error:
        _xfail_live_transport_error(error)
        raise

    assert "http_headers" in result
    assert isinstance(result.http_headers, dict)
    assert "total_usage" in result


def test_online_send_dry_run() -> None:
    """Validate a send payload against the live API without delivering it."""
    from_address = os.environ.get("MAILCHANNELS_ONLINE_FROM")
    to_address = os.environ.get("MAILCHANNELS_ONLINE_TO")
    if not from_address or not to_address:
        pytest.skip(
            "set MAILCHANNELS_ONLINE_FROM and MAILCHANNELS_ONLINE_TO to run "
            "dry-run send"
        )

    try:
        result = _client().emails.send(
            _send_payload(
                from_address,
                to_address,
                subject="MailChannels SDK online dry-run test",
                body="This dry-run validates SDK online testing without delivery.",
            ),
            dry_run=True,
        )
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except requests.RequestException as error:
        _xfail_live_transport_error(error)
        raise

    assert "http_headers" in result
    assert isinstance(result.http_headers, dict)


def test_online_send_real_email() -> None:
    """Send a real email through the live API when explicitly enabled."""
    if os.environ.get("MAILCHANNELS_ONLINE_SEND_REAL") != "1":
        pytest.skip("set MAILCHANNELS_ONLINE_SEND_REAL=1 to send a real email")
    from_address = os.environ.get("MAILCHANNELS_ONLINE_FROM")
    to_address = os.environ.get("MAILCHANNELS_ONLINE_TO")
    if not from_address or not to_address:
        pytest.skip(
            "set MAILCHANNELS_ONLINE_FROM and MAILCHANNELS_ONLINE_TO to send "
            "a real email"
        )

    subject = "MailChannels SDK real online send test"
    body = (
        "This is a real email sent by the MailChannels Python SDK online test at "
        f"{datetime.now(timezone.utc).isoformat()}."
    )
    try:
        result = _client().emails.send(
            _send_payload(from_address, to_address, subject=subject, body=body),
        )
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except requests.RequestException as error:
        _xfail_live_transport_error(error)
        raise

    assert "http_headers" in result
    assert isinstance(result.http_headers, dict)


def test_online_metrics_volume() -> None:
    """Retrieve live volume metrics with a narrow default query."""
    try:
        result = _client().metrics.volume(interval="day")
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except requests.RequestException as error:
        _xfail_live_transport_error(error)
        raise

    assert "http_headers" in result
    assert isinstance(result.http_headers, dict)


def test_online_sub_accounts_list() -> None:
    """Retrieve a small page of live sub-accounts."""
    try:
        result = _client().sub_accounts.list(limit=1, offset=0)
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except requests.RequestException as error:
        _xfail_live_transport_error(error)
        raise

    assert "http_headers" in result
    assert isinstance(result.http_headers, dict)


def test_online_suppression_list() -> None:
    """Retrieve a small page of live suppression entries."""
    try:
        result = _client().suppressions.list(limit=1, offset=0)
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except requests.RequestException as error:
        _xfail_live_transport_error(error)
        raise

    assert "http_headers" in result
    assert isinstance(result.http_headers, dict)


def test_online_webhooks_list() -> None:
    """Retrieve live configured webhooks without modifying them."""
    try:
        result = _client().webhooks.list()
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except requests.RequestException as error:
        _xfail_live_transport_error(error)
        raise

    assert "http_headers" in result
    assert isinstance(result.http_headers, dict)


def test_online_dkim_list_for_domain() -> None:
    """Retrieve live DKIM keys for an explicitly configured test domain."""
    domain = os.environ.get("MAILCHANNELS_ONLINE_DOMAIN")
    if not domain:
        pytest.skip("set MAILCHANNELS_ONLINE_DOMAIN to list live DKIM keys")

    try:
        result = _client().dkim.list(domain, limit=1)
    except mailchannels.ApiError as error:
        _xfail_live_server_error(error)
        raise
    except requests.RequestException as error:
        _xfail_live_transport_error(error)
        raise

    assert "http_headers" in result
    assert isinstance(result.http_headers, dict)


def _send_payload(
    from_address: str,
    to_address: str,
    *,
    subject: str,
    body: str,
) -> dict[str, Any]:
    """Build a live send payload."""
    return {
        "from": {"email": from_address},
        "to": [{"email": to_address}],
        "subject": subject,
        "text": body,
    }


def _xfail_live_server_error(error: mailchannels.ApiError) -> None:
    """Mark live MailChannels 5xx responses as external service failures."""
    if error.status_code is not None and error.status_code >= 500:
        pytest.xfail(
            "Live MailChannels API returned a server error: "
            f"status={error.status_code} request_id={error.request_id}"
        )


def _xfail_live_transport_error(error: BaseException) -> None:
    """Mark live network or timeout failures as external test conditions."""
    pytest.xfail(f"Live MailChannels API transport failed: {error}")


def _httpx_http_error() -> type[BaseException]:
    """Return the base httpx transport exception type."""
    import httpx

    return httpx.HTTPError
