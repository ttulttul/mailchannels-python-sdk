"""Tests for client configuration and response ergonomics."""

from __future__ import annotations

import pytest
from conftest import FakeRequestsClient

import mailchannels
from mailchannels.client import Client
from mailchannels.response import SDKResponse
from mailchannels.usage import UsageStats


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


def test_non_strict_responses_keep_dict_ergonomics() -> None:
    """It keeps dict-like responses by default even when a response model exists."""
    transport = FakeRequestsClient(SDKResponse(200, {"total_usage": 42}, "{}"))
    client = Client(api_key="test-key", http_client=transport)

    result = client.usage.retrieve()

    assert isinstance(result, dict)
    assert result.total_usage == 42


def test_strict_responses_return_pydantic_models() -> None:
    """It returns typed response models when strict response parsing is enabled."""
    transport = FakeRequestsClient(
        SDKResponse(
            200,
            {"total_usage": 42},
            "{}",
            headers={"X-Request-ID": "req_123"},
        )
    )
    client = Client(
        api_key="test-key",
        http_client=transport,
        strict_responses=True,
    )

    result = client.usage.retrieve()

    assert isinstance(result, UsageStats)
    assert result.total_usage == 42
    assert result.http_headers == {"X-Request-ID": "req_123"}


def test_strict_responses_raise_validation_errors() -> None:
    """It raises a structured SDK error when a typed response cannot be parsed."""
    transport = FakeRequestsClient(SDKResponse(200, {"period_start_date": "x"}, "{}"))
    client = Client(
        api_key="test-key",
        http_client=transport,
        strict_responses=True,
    )

    with pytest.raises(mailchannels.ResponseValidationError) as error:
        client.usage.retrieve()

    assert error.value.code == "ResponseValidationError"
    assert error.value.error_type == "response_validation_error"
    assert error.value.response["period_start_date"] == "x"


def test_module_level_strict_response_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It supports strict response models through module-level configuration."""
    transport = FakeRequestsClient(SDKResponse(200, {"total_usage": 7}, "{}"))
    monkeypatch.setattr(mailchannels, "api_key", "module-key")
    monkeypatch.setattr(mailchannels, "default_http_client", transport)
    monkeypatch.setattr(mailchannels, "strict_responses", True)

    result = mailchannels.Usage.retrieve()

    assert isinstance(result, UsageStats)
    assert result.total_usage == 7


def test_user_agent_uses_exported_version() -> None:
    """It builds the User-Agent from exported package version metadata."""
    transport = FakeRequestsClient()
    client = Client(api_key="test-key", http_client=transport)

    client.emails.queue(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Hello",
        }
    )

    assert mailchannels.__version__ == "0.1.0"
    assert mailchannels.get_version() == mailchannels.__version__
    assert transport.calls[0]["headers"]["User-Agent"] == (
        f"mailchannels-python/{mailchannels.__version__}"
    )


def test_module_level_api_accepts_custom_http_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It accepts any sync transport matching the public protocol."""

    class CustomTransport:
        """Custom transport that satisfies SyncHTTPClient."""

        def __init__(self) -> None:
            """Create a custom test transport."""
            self.calls: list[dict[str, object]] = []

        def request(
            self,
            method: str,
            url: str,
            *,
            headers: dict[str, str],
            json: dict[str, object] | None = None,
            params: dict[str, object] | None = None,
        ) -> SDKResponse:
            """Record a request and return a successful response."""
            self.calls.append(
                {
                    "method": method,
                    "url": url,
                    "headers": headers,
                    "json": json,
                    "params": params,
                }
            )
            return SDKResponse(202, {"id": "custom_123"}, "{}")

    transport = CustomTransport()
    monkeypatch.setattr(mailchannels, "api_key", "module-key")
    monkeypatch.setattr(mailchannels, "default_http_client", transport)

    result = mailchannels.Emails.queue(
        {
            "from": {"email": "sender@example.com"},
            "to": "recipient@example.net",
            "subject": "Hello",
            "text": "Hello",
        }
    )

    assert result.id == "custom_123"
    assert transport.calls[0]["headers"]["X-Api-Key"] == "module-key"
