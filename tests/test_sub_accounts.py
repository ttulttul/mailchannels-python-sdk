"""Tests for sub-account resources."""

from __future__ import annotations

import pytest
from conftest import FakeHTTPXClient, FakeRequestsClient

from mailchannels import MailChannelsError
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

    client.sub_accounts.list(limit=25, offset=5)
    client.sub_accounts.api_keys.create("clienta")
    client.sub_accounts.smtp_passwords.create("clienta")
    client.sub_accounts.limits.set("clienta", sends=100_000)
    client.sub_accounts.limits.retrieve("clienta")
    client.sub_accounts.limits.delete("clienta")
    client.sub_accounts.retrieve_usage("clienta")

    expected_limit_url = "https://api.mailchannels.net/tx/v1/sub-account/clienta/limit"
    assert [(call["method"], call["url"]) for call in transport.calls] == [
        ("GET", "https://api.mailchannels.net/tx/v1/sub-account"),
        ("POST", "https://api.mailchannels.net/tx/v1/sub-account/clienta/api-key"),
        (
            "POST",
            "https://api.mailchannels.net/tx/v1/sub-account/clienta/smtp-password",
        ),
        ("PUT", expected_limit_url),
        ("GET", expected_limit_url),
        ("DELETE", expected_limit_url),
        ("GET", "https://api.mailchannels.net/tx/v1/sub-account/clienta/usage"),
    ]
    assert transport.calls[0]["params"] == {"limit": 25, "offset": 5}
    assert transport.calls[3]["json"] == {"sends": 100_000}


def test_sub_account_limit_keeps_monthly_limit_alias() -> None:
    """It maps the old monthly_limit argument to the documented sends payload."""
    transport = FakeRequestsClient()
    client = Client(api_key="test-key", http_client=transport)

    client.sub_accounts.limits.set("clienta", monthly_limit=50_000)

    assert transport.calls[0]["method"] == "PUT"
    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/sub-account/clienta/limit"
    )
    assert transport.calls[0]["json"] == {"sends": 50_000}


def test_sub_account_limit_rejects_ambiguous_limit_arguments() -> None:
    """It rejects calls that pass both legacy and documented limit names."""
    client = Client(api_key="test-key", http_client=FakeRequestsClient())

    with pytest.raises(MailChannelsError) as error:
        client.sub_accounts.limits.set(
            "clienta",
            sends=50_000,
            monthly_limit=50_000,
        )

    assert error.value.code == "InvalidLimitParameters"


async def test_sub_account_async_methods_use_async_transport() -> None:
    """It exposes async sub-account operations."""
    transport = FakeHTTPXClient(SDKResponse(200, {"sub_accounts": []}, "{}"))
    client = Client(api_key="test-key", async_http_client=transport)

    await client.sub_accounts.list_async(limit=25, offset=5)
    await client.sub_accounts.limits.retrieve_async("clienta")

    assert [call["url"] for call in transport.calls] == [
        "https://api.mailchannels.net/tx/v1/sub-account",
        "https://api.mailchannels.net/tx/v1/sub-account/clienta/limit",
    ]
    assert transport.calls[0]["params"] == {"limit": 25, "offset": 5}
