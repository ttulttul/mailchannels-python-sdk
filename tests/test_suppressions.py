"""Tests for suppression list resources."""

from __future__ import annotations

from conftest import FakeHTTPXClient, FakeRequestsClient

from mailchannels.client import Client
from mailchannels.response import SDKResponse


def test_suppression_list_uses_filters() -> None:
    """It retrieves suppression entries with documented filters."""
    transport = FakeRequestsClient(
        SDKResponse(200, {"suppression_list": [{"recipient": "a@example.net"}]}, "{}")
    )
    client = Client(api_key="test-key", http_client=transport)

    result = client.suppressions.list(
        recipient="a@example.net",
        source="api",
        created_after="2026-04-01",
        limit=10,
        offset=0,
    )

    assert result.suppression_list == [{"recipient": "a@example.net"}]
    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/suppression-list"
    )
    assert transport.calls[0]["params"] == {
        "recipient": "a@example.net",
        "source": "api",
        "created_after": "2026-04-01",
        "limit": 10,
        "offset": 0,
    }


def test_create_and_delete_suppression_entries() -> None:
    """It creates and deletes suppression entries."""
    transport = FakeRequestsClient(SDKResponse(201, None, ""))
    client = Client(api_key="test-key", http_client=transport)

    client.suppressions.create(
        [
            {
                "recipient": "a@example.net",
                "suppression_types": ["non-transactional"],
            }
        ],
        add_to_sub_accounts=True,
    )
    client.suppressions.delete("a@example.net", source="all")

    assert transport.calls[0]["method"] == "POST"
    assert transport.calls[0]["json"] == {
        "suppression_entries": [
            {
                "recipient": "a@example.net",
                "suppression_types": ["non-transactional"],
            }
        ],
        "add_to_sub_accounts": True,
    }
    assert transport.calls[1]["method"] == "DELETE"
    assert transport.calls[1]["url"] == (
        "https://api.mailchannels.net/tx/v1/suppression-list/recipients/a@example.net"
    )
    assert transport.calls[1]["params"] == {"source": "all"}


async def test_suppression_async_methods_use_async_transport() -> None:
    """It exposes async suppression operations."""
    transport = FakeHTTPXClient(SDKResponse(200, {"suppression_list": []}, "{}"))
    client = Client(api_key="test-key", async_http_client=transport)

    await client.suppressions.list_async(limit=5)

    assert transport.calls[0]["method"] == "GET"
    assert transport.calls[0]["params"] == {"limit": 5}
