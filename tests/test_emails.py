"""Tests for email sending resources."""

from __future__ import annotations

import pytest
from conftest import FakeHTTPXClient, FakeRequestsClient

import mailchannels
from mailchannels.client import Client
from mailchannels.emails import (
    UNSUBSCRIBE_URL_PLACEHOLDER,
    Content,
    EmailAddress,
    EmailParams,
    normalize_email_params,
)
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


def test_normalize_top_level_custom_headers() -> None:
    """It preserves top-level custom headers in shortcut payloads."""
    payload = normalize_email_params(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Custom Header Example",
            "text": "This email includes custom headers.",
            "headers": {
                "List-Unsubscribe": "<mailto:unsubscribe@example.com>",
                "X-Campaign-ID": "newsletter-123",
            },
        }
    )

    assert payload["headers"] == {
        "List-Unsubscribe": "<mailto:unsubscribe@example.com>",
        "X-Campaign-ID": "newsletter-123",
    }


def test_normalize_personalization_custom_headers() -> None:
    """It preserves recipient-specific custom headers."""
    payload = normalize_email_params(
        {
            "from": {"email": "sender@example.com"},
            "personalizations": [
                {
                    "to": [{"email": "banana-lover@example.net"}],
                    "subject": "Bananas Are On Sale",
                    "headers": {
                        "List-Unsubscribe": "<mailto:unsubscribe@bananas.example>",
                        "X-Custom-Header": "BananaFan123",
                    },
                },
                {
                    "to": [{"email": "apple-lover@example.net"}],
                    "subject": "Apples Are On Sale",
                    "headers": {
                        "List-Unsubscribe": "<mailto:unsubscribe@apples.example>",
                        "X-Custom-Header": "AppleFan123",
                    },
                },
            ],
            "subject": "Sale",
            "text": "This email includes custom headers.",
        }
    )

    assert payload["personalizations"][0]["headers"] == {
        "List-Unsubscribe": "<mailto:unsubscribe@bananas.example>",
        "X-Custom-Header": "BananaFan123",
    }
    assert payload["personalizations"][1]["headers"] == {
        "List-Unsubscribe": "<mailto:unsubscribe@apples.example>",
        "X-Custom-Header": "AppleFan123",
    }


def test_normalize_mailchannels_template_payload() -> None:
    """It preserves MailChannels mustache template fields."""
    payload = normalize_email_params(
        {
            "from": {"email": "sender@example.com"},
            "personalizations": [
                {
                    "to": [{"email": "recipient1@example.net"}],
                    "dynamic_template_data": {"name": "Jane Doe"},
                },
                {
                    "to": [{"email": "recipient2@example.net"}],
                    "dynamic_template_data": {"name": "John Smith"},
                },
            ],
            "subject": "Template Example",
            "content": [
                {
                    "type": "text/plain",
                    "value": "Hello {{name}}",
                    "template_type": "mustache",
                }
            ],
        }
    )

    assert payload["content"] == [
        {
            "type": "text/plain",
            "value": "Hello {{name}}",
            "template_type": "mustache",
        }
    ]
    assert payload["personalizations"][0]["dynamic_template_data"] == {
        "name": "Jane Doe"
    }


def test_normalize_pydantic_template_params() -> None:
    """It supports typed template content and dynamic template data."""
    params = EmailParams(
        from_=EmailAddress(email="sender@example.com"),
        personalizations=[
            {
                "to": [{"email": "recipient@example.net"}],
                "dynamic_template_data": {"name": {"first": "Jane", "last": "Doe"}},
            }
        ],
        subject="Template Example",
        content=[
            Content(
                type="text/html",
                value="Hello {{name.first}} {{name.last}}",
                template_type="mustache",
            )
        ],
    )

    payload = normalize_email_params(params)

    assert payload["content"][0]["template_type"] == "mustache"
    assert payload["personalizations"][0]["dynamic_template_data"] == {
        "name": {"first": "Jane", "last": "Doe"}
    }


def test_normalize_unsubscribe_link_template_payload() -> None:
    """It preserves the MailChannels unsubscribe placeholder in templates."""
    payload = normalize_email_params(
        {
            "from": {"email": "sender@example.com"},
            "personalizations": [{"to": [{"email": "recipient@example.net"}]}],
            "subject": "Unsubscribe Example",
            "content": [
                {
                    "type": "text/html",
                    "value": (
                        "<a href='"
                        f"{UNSUBSCRIBE_URL_PLACEHOLDER}"
                        "'>unsubscribe</a>"
                    ),
                    "template_type": "mustache",
                }
            ],
        }
    )

    assert payload["content"][0]["value"] == (
        "<a href='{{mc-unsubscribe-url}}'>unsubscribe</a>"
    )
    assert payload["content"][0]["template_type"] == "mustache"


def test_normalize_list_unsubscribe_payload() -> None:
    """It preserves fields needed for automatic List-Unsubscribe headers."""
    payload = normalize_email_params(
        {
            "from": {"email": "sender@example.com"},
            "personalizations": [
                {
                    "to": [{"email": "recipient@example.net"}],
                    "dkim_domain": "example.com",
                    "dkim_selector": "mailchannels",
                    "dkim_private_key": "-----BEGIN PRIVATE KEY-----",
                }
            ],
            "subject": "Marketing Example",
            "text": "Hello",
            "transactional": False,
        }
    )

    assert payload["transactional"] is False
    assert payload["personalizations"][0]["dkim_domain"] == "example.com"
    assert payload["personalizations"][0]["dkim_selector"] == "mailchannels"
    assert payload["personalizations"][0]["dkim_private_key"] == (
        "-----BEGIN PRIVATE KEY-----"
    )


def test_normalize_root_dkim_payload() -> None:
    """It preserves root DKIM signing fields in send payloads."""
    payload = normalize_email_params(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "DKIM Example",
            "text": "This message is signed with DKIM.",
            "dkim_domain": "example.com",
            "dkim_selector": "mcdkim",
            "dkim_private_key": "BASE64_PRIVATE_KEY",
        }
    )

    assert payload["dkim_domain"] == "example.com"
    assert payload["dkim_selector"] == "mcdkim"
    assert payload["dkim_private_key"] == "BASE64_PRIVATE_KEY"


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

    assert result.id == "queued_123"
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

    assert result.id == "queued_123"
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
