"""Online tests for the live MailChannels Email API."""

from __future__ import annotations

import os
from typing import Any

import pytest

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

    result = _client().emails.send(
        _dry_run_payload(from_address, to_address),
        dry_run=True,
    )

    assert "http_headers" in result
    assert isinstance(result.http_headers, dict)


def _dry_run_payload(from_address: str, to_address: str) -> dict[str, Any]:
    """Build a live dry-run send payload."""
    return {
        "from": {"email": from_address},
        "to": [{"email": to_address}],
        "subject": "MailChannels SDK online dry-run test",
        "text": "This dry-run validates SDK online testing without delivery.",
    }


def _xfail_live_server_error(error: mailchannels.ApiError) -> None:
    """Mark live MailChannels 5xx responses as external service failures."""
    if error.status_code is not None and error.status_code >= 500:
        pytest.xfail(
            "Live MailChannels API returned a server error: "
            f"status={error.status_code} request_id={error.request_id}"
        )
