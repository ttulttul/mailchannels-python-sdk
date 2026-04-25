"""Tests for DKIM resources."""

from __future__ import annotations

import pytest
from conftest import FakeHTTPXClient, FakeRequestsClient

import mailchannels
from mailchannels.client import Client
from mailchannels.response import SDKResponse


def test_create_dkim_key_uses_expected_path_and_payload() -> None:
    """It creates MailChannels-hosted DKIM key pairs."""
    transport = FakeRequestsClient(
        SDKResponse(
            201,
            {
                "domain": "example.com",
                "selector": "mcdkim",
                "public_key": "PUBLIC_KEY",
                "status": "active",
                "algorithm": "rsa",
                "dkim_dns_records": [
                    {
                        "name": "mcdkim._domainkey.example.com",
                        "type": "TXT",
                        "value": "v=DKIM1;p=PUBLIC_KEY",
                    }
                ],
            },
            "{}",
        )
    )
    client = Client(api_key="test-key", http_client=transport)

    result = client.dkim.create(
        "example.com",
        selector="mcdkim",
        algorithm="rsa",
        key_length=2048,
    )

    assert result["selector"] == "mcdkim"
    assert transport.calls[0]["method"] == "POST"
    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/domains/example.com/dkim-keys"
    )
    assert transport.calls[0]["json"] == {
        "selector": "mcdkim",
        "algorithm": "rsa",
        "key_length": 2048,
    }


def test_list_dkim_keys_uses_filters() -> None:
    """It retrieves DKIM keys with optional filters and DNS records."""
    transport = FakeRequestsClient(SDKResponse(200, {"keys": []}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    client.dkim.list(
        "example.com",
        selector="mcdkim",
        status="active",
        offset=0,
        limit=10,
        include_dns_record=True,
    )

    assert transport.calls[0]["method"] == "GET"
    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/domains/example.com/dkim-keys"
    )
    assert transport.calls[0]["params"] == {
        "selector": "mcdkim",
        "status": "active",
        "offset": 0,
        "limit": 10,
        "include_dns_record": True,
    }


def test_update_and_rotate_dkim_keys_use_documented_paths() -> None:
    """It updates DKIM status and rotates keys using the OpenAPI paths."""
    transport = FakeRequestsClient(SDKResponse(204, None, ""))
    client = Client(api_key="test-key", http_client=transport)

    client.dkim.update_status("example.com", "mcdkim", status="rotated")
    client.dkim.rotate("example.com", "mcdkim", new_selector="mcdkim2")

    assert [call["url"] for call in transport.calls] == [
        "https://api.mailchannels.net/tx/v1/domains/example.com/dkim-keys/mcdkim",
        (
            "https://api.mailchannels.net/tx/v1/domains/example.com/"
            "dkim-keys/mcdkim/rotate"
        ),
    ]
    assert transport.calls[0]["method"] == "PATCH"
    assert transport.calls[0]["json"] == {"status": "rotated"}
    assert transport.calls[1]["method"] == "POST"
    assert transport.calls[1]["json"] == {"new_key": {"selector": "mcdkim2"}}


def test_module_level_dkim_api_uses_global_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It supports module-level DKIM calls."""
    transport = FakeRequestsClient(SDKResponse(200, {"keys": []}, "{}"))
    monkeypatch.setattr(mailchannels, "api_key", "module-key")
    monkeypatch.setattr(mailchannels, "default_http_client", transport)

    mailchannels.Dkim.list("example.com")

    assert transport.calls[0]["headers"]["X-Api-Key"] == "module-key"
    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/domains/example.com/dkim-keys"
    )


async def test_dkim_async_methods_use_async_transport() -> None:
    """It exposes async DKIM operations."""
    transport = FakeHTTPXClient(SDKResponse(200, {"keys": []}, "{}"))
    client = Client(api_key="test-key", async_http_client=transport)

    await client.dkim.list_async("example.com", limit=1)

    assert transport.calls[0]["method"] == "GET"
    assert transport.calls[0]["params"] == {"limit": 1}
