"""Tests for client configuration and response ergonomics."""

from __future__ import annotations

import pytest
from conftest import FakeRequestsClient

import mailchannels
from mailchannels.client import Client
from mailchannels.response import SDKResponse


def test_client_reads_environment_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It reads API key and API URL from environment variables."""
    monkeypatch.setenv("MAILCHANNELS_API_KEY", "env-key")
    monkeypatch.setenv("MAILCHANNELS_API_URL", "https://example.test/api")
    monkeypatch.setattr(mailchannels, "api_key", None)
    monkeypatch.setattr(mailchannels, "base_url", "")
    transport = FakeRequestsClient()

    client = Client(http_client=transport)
    client.emails.queue(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Hello",
        }
    )

    assert transport.calls[0]["headers"]["X-Api-Key"] == "env-key"
    assert transport.calls[0]["url"] == "https://example.test/api/send-async"


def test_response_supports_headers_and_attribute_access() -> None:
    """It exposes response body keys as attributes and preserves HTTP headers."""
    transport = FakeRequestsClient(
        SDKResponse(
            202,
            {"id": "queued_123"},
            "{}",
            headers={"X-Request-ID": "req_123"},
        )
    )
    client = Client(api_key="test-key", http_client=transport)

    result = client.emails.queue(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Hello",
        }
    )

    assert result.id == "queued_123"
    assert result["id"] == "queued_123"
    assert result.http_headers["X-Request-ID"] == "req_123"
