"""Tests for email sending resources."""

from __future__ import annotations

import pytest
from conftest import FakeHTTPXClient, FakeRequestsClient

import mailchannels
from mailchannels.client import Client
from mailchannels.emails import EmailAddress, EmailParams, normalize_email_params
from mailchannels.response import SDKResponse


def test_normalize_resend_style_email_shortcuts() -> None:
    """It converts simple SDK shortcuts into MailChannels JSON."""
    payload = normalize_email_params(
        {
            "from": {"email": "sender@example.com", "name": "Sender"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Plain text",
            "html": "<strong>Hello</strong>",
        }
    )

    assert payload == {
        "from": {"email": "sender@example.com", "name": "Sender"},
        "personalizations": [{"to": [{"email": "recipient@example.net"}]}],
        "subject": "Hello",
        "content": [
            {"type": "text/plain", "value": "Plain text"},
            {"type": "text/html", "value": "<strong>Hello</strong>"},
        ],
    }


def test_normalize_pydantic_email_params() -> None:
    """It accepts MailChannels-native Pydantic models."""
    params = EmailParams(
        from_=EmailAddress(email="sender@example.com"),
        personalizations=[{"to": [{"email": "recipient@example.net"}]}],
        subject="Hello",
        content=[{"type": "text/plain", "value": "Plain text"}],
    )

    assert normalize_email_params(params)["from"] == {"email": "sender@example.com"}


def test_queue_uses_send_async_endpoint() -> None:
    """It posts queued sends to the MailChannels /send-async endpoint."""
    transport = FakeRequestsClient()
    client = Client(api_key="test-key", http_client=transport)

    result = client.emails.queue(
        {
            "from": {"email": "sender@example.com"},
            "to": [{"email": "recipient@example.net"}],
            "subject": "Hello",
            "text": "Plain text",
        }
    )

    assert result == {"id": "queued_123"}
    call = transport.calls[0]
    assert call["method"] == "POST"
    assert call["url"] == "https://api.mailchannels.net/tx/v1/send-async"
    assert call["headers"]["X-Api-Key"] == "test-key"
    assert call["json"]["content"] == [{"type": "text/plain", "value": "Plain text"}]


def test_send_supports_dry_run_query() -> None:
    """It sends dry-run validation through the documented query parameter."""
    transport = FakeRequestsClient(SDKResponse(200, {"dry_run": True}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    client.emails.send(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Plain text",
        },
        dry_run=True,
    )

    assert transport.calls[0]["url"] == "https://api.mailchannels.net/tx/v1/send"
    assert transport.calls[0]["params"] == {"dry-run": "true"}


@pytest.mark.asyncio
async def test_queue_async_uses_async_transport() -> None:
    """It can queue a message with async HTTP."""
    transport = FakeHTTPXClient()
    client = Client(api_key="test-key", async_http_client=transport)

    result = await client.emails.queue_async(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Plain text",
        }
    )

    assert result == {"id": "queued_123"}
    assert transport.calls[0]["url"] == "https://api.mailchannels.net/tx/v1/send-async"


def test_module_level_email_api_uses_global_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It supports the Resend-style module-level API."""
    transport = FakeRequestsClient()
    monkeypatch.setattr(mailchannels, "api_key", "module-key")
    monkeypatch.setattr(mailchannels, "default_http_client", transport)

    mailchannels.Emails.queue(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Plain text",
        }
    )

    assert transport.calls[0]["headers"]["X-Api-Key"] == "module-key"
