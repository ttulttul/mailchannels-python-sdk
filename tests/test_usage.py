"""Tests for usage resources."""

from __future__ import annotations

import pytest
from conftest import FakeHTTPXClient, FakeRequestsClient

import mailchannels
from mailchannels.client import Client
from mailchannels.response import SDKResponse


def test_usage_retrieve_uses_top_level_usage_endpoint() -> None:
    """It retrieves parent-account usage stats."""
    transport = FakeRequestsClient(
        SDKResponse(
            200,
            {
                "total_usage": 5000,
                "period_start_date": "2026-04-01",
                "period_end_date": "2026-04-30",
            },
            "{}",
        )
    )
    client = Client(api_key="test-key", http_client=transport)

    result = client.usage.retrieve()

    assert result.total_usage == 5000
    assert transport.calls[0]["method"] == "GET"
    assert transport.calls[0]["url"] == "https://api.mailchannels.net/tx/v1/usage"


async def test_usage_retrieve_async_uses_async_transport() -> None:
    """It retrieves parent-account usage stats using async HTTP."""
    transport = FakeHTTPXClient(SDKResponse(200, {"total_usage": 5000}, "{}"))
    client = Client(api_key="test-key", async_http_client=transport)

    result = await client.usage.retrieve_async()

    assert result.total_usage == 5000
    assert transport.calls[0]["method"] == "GET"
    assert transport.calls[0]["url"] == "https://api.mailchannels.net/tx/v1/usage"


def test_module_level_usage_api_uses_global_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It supports module-level usage calls."""
    transport = FakeRequestsClient(SDKResponse(200, {"total_usage": 1}, "{}"))
    monkeypatch.setattr(mailchannels, "api_key", "module-key")
    monkeypatch.setattr(mailchannels, "default_http_client", transport)

    mailchannels.Usage.retrieve()

    assert transport.calls[0]["headers"]["X-Api-Key"] == "module-key"
    assert transport.calls[0]["url"] == "https://api.mailchannels.net/tx/v1/usage"
