"""Tests for domain configuration checks."""

from __future__ import annotations

import pytest
from conftest import FakeHTTPXClient, FakeRequestsClient

import mailchannels
from mailchannels.check_domain import CheckDomain
from mailchannels.client import Client
from mailchannels.domain_checks import DkimSetting
from mailchannels.response import SDKResponse


def test_domain_check_posts_expected_payload() -> None:
    """It checks a domain using the documented `/check-domain` endpoint."""
    transport = FakeRequestsClient(
        SDKResponse(
            200,
            {"check_results": {"spf": {"verdict": "passed"}}},
            "{}",
        )
    )
    client = Client(api_key="test-key", http_client=transport)

    result = client.domain_checks.check(
        "example.com",
        sender_id="sender-123",
        dkim_settings=[
            DkimSetting(dkim_domain="example.com", dkim_selector="mcdkim"),
            {"dkim_selector": "other"},
        ],
    )

    assert result.check_results["spf"]["verdict"] == "passed"
    assert transport.calls[0]["method"] == "POST"
    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/check-domain"
    )
    assert transport.calls[0]["json"] == {
        "domain": "example.com",
        "sender_id": "sender-123",
        "dkim_settings": [
            {"dkim_domain": "example.com", "dkim_selector": "mcdkim"},
            {"dkim_selector": "other"},
        ],
    }


def test_check_domain_alias_posts_expected_payload() -> None:
    """It exposes `/check-domain` through the documented endpoint name."""
    transport = FakeRequestsClient(SDKResponse(200, {"references": []}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    client.check_domain.check("example.com")

    assert client.check_domain is client.domain_checks
    assert transport.calls[0]["method"] == "POST"
    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/check-domain"
    )
    assert transport.calls[0]["json"] == {"domain": "example.com"}


async def test_domain_check_async_uses_async_transport() -> None:
    """It checks a domain using async HTTP."""
    transport = FakeHTTPXClient(SDKResponse(200, {"references": []}, "{}"))
    client = Client(api_key="test-key", async_http_client=transport)

    await client.domain_checks.check_async("example.com")

    assert transport.calls[0]["method"] == "POST"
    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/check-domain"
    )
    assert transport.calls[0]["json"] == {"domain": "example.com"}


def test_domain_check_module_level_proxy_uses_default_client(monkeypatch) -> None:
    """It exposes module-level domain check operations."""
    transport = FakeRequestsClient(SDKResponse(200, {"references": []}, "{}"))
    monkeypatch.setattr(mailchannels, "api_key", "test-key")
    monkeypatch.setattr(mailchannels, "default_http_client", transport)

    mailchannels.DomainChecks.check("example.com")

    assert transport.calls[0]["url"] == (
        "https://api.mailchannels.net/tx/v1/check-domain"
    )


def test_check_domain_module_alias_uses_default_client(monkeypatch) -> None:
    """It exposes a top-level CheckDomain alias for discoverability."""
    transport = FakeRequestsClient(SDKResponse(200, {"references": []}, "{}"))
    monkeypatch.setattr(mailchannels, "api_key", "test-key")
    monkeypatch.setattr(mailchannels, "default_http_client", transport)

    mailchannels.CheckDomain.check("example.com")
    CheckDomain.check("example.net")

    assert [call["json"] for call in transport.calls] == [
        {"domain": "example.com"},
        {"domain": "example.net"},
    ]


def test_domain_check_rejects_more_than_ten_dkim_settings() -> None:
    """It enforces the OpenAPI maximum of ten DKIM settings."""
    client = Client(api_key="test-key", http_client=FakeRequestsClient())

    with pytest.raises(mailchannels.MailChannelsError) as error:
        client.domain_checks.check(
            "example.com",
            dkim_settings=[{"dkim_selector": str(index)} for index in range(11)],
        )

    assert error.value.code == "InvalidDomainCheckParameters"
