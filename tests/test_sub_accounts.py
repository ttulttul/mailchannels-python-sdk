"""Tests for sub-account resources."""

from __future__ import annotations

from conftest import FakeHTTPXClient, FakeRequestsClient

from mailchannels.client import Client
from mailchannels.response import SDKResponse


def test_create_sub_account_posts_expected_payload() -> None:
    """It creates sub-accounts with the documented fields."""
    transport = FakeRequestsClient(SDKResponse(201, {"handle": "clienta"}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    result = client.sub_accounts.create(company_name="Client A", handle="clienta")

    assert result["handle"] == "clienta"
    assert transport.calls[0]["method"] == "POST"
    assert transport.calls[0]["url"] == "https://api.mailchannels.net/tx/v1/sub-account"
    assert transport.calls[0]["json"] == {
        "company_name": "Client A",
        "handle": "clienta",
    }


def test_sub_account_nested_resources_use_expected_paths() -> None:
    """It exposes API key, SMTP password, limit, and usage endpoints."""
    transport = FakeRequestsClient()
    client = Client(api_key="test-key", http_client=transport)

    client.sub_accounts.api_keys.create("clienta")
    client.sub_accounts.smtp_passwords.create("clienta")
    client.sub_accounts.limits.set("clienta", monthly_limit=100_000)
    client.sub_accounts.retrieve_usage("clienta")

    assert [call["url"] for call in transport.calls] == [
        "https://api.mailchannels.net/tx/v1/sub-account/clienta/api-key",
        "https://api.mailchannels.net/tx/v1/sub-account/clienta/smtp-password",
        "https://api.mailchannels.net/tx/v1/sub-account/clienta/limits",
        "https://api.mailchannels.net/tx/v1/sub-account/clienta/usage",
    ]
    assert transport.calls[2]["json"] == {"monthly_limit": 100_000}


async def test_sub_account_async_methods_use_async_transport() -> None:
    """It exposes async sub-account operations."""
    transport = FakeHTTPXClient(SDKResponse(200, {"sub_accounts": []}, "{}"))
    client = Client(api_key="test-key", async_http_client=transport)

    await client.sub_accounts.list_async()
    await client.sub_accounts.limits.retrieve_async("clienta")

    assert [call["url"] for call in transport.calls] == [
        "https://api.mailchannels.net/tx/v1/sub-account",
        "https://api.mailchannels.net/tx/v1/sub-account/clienta/limits",
    ]
